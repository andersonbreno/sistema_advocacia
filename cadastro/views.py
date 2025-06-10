# Importações necessárias para o funcionamento das views
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction


# Importações dos modelos
from clientes.models import Cliente
from processos.models import Processo
from tarefas.models import Tarefa


# Importações dos formulários
from clientes.forms import ClienteForm
from processos.forms import ProcessoForm
from tarefas.forms import TarefaForm

# CadastroCreateView
class CadastroCreateView(LoginRequiredMixin, CreateView):
    """
    View para cadastro em etapas de Cliente → Processo → Tarefa
    Utiliza sessão para persistência entre requisições e transações atômicas
    """
    model = Cliente
    form_class = ClienteForm
    template_name = "cadastro/create.html"
    success_url = reverse_lazy("cadastro:list")
    
    # Chaves para armazenamento na sessão
    SESSION_KEYS = {
        'cliente_data': 'wizard_cliente_data',
        'processo_data': 'wizard_processo_data',
        'cliente_id': 'wizard_cliente_id',
        'processo_id': 'wizard_processo_id',
        'current_step': 'wizard_current_step'
    }

    def dispatch(self, request, *args, **kwargs):
        """Inicializa ou limpa a sessão conforme necessário"""
        if request.method == 'GET':
            self.clear_session_data()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """Prepara o contexto com forms e dados da sessão"""
        context = super().get_context_data(**kwargs)
        
        # Recupera dados da sessão
        session_data = {
            'cliente_data': self.request.session.get(self.SESSION_KEYS['cliente_data']),
            'processo_data': self.request.session.get(self.SESSION_KEYS['processo_data']),
            'cliente_id': self.request.session.get(self.SESSION_KEYS['cliente_id']),
            'processo_id': self.request.session.get(self.SESSION_KEYS['processo_id']),
            'current_step': self.request.session.get(self.SESSION_KEYS['current_step'], 'cliente')
        }

        # Inicializa forms com dados da sessão quando disponíveis
        if self.request.POST:
            context['processo_form'] = ProcessoForm(
                self.request.POST,
                prefix='processo',
                initial=session_data['processo_data']
            )
            context['tarefa_form'] = TarefaForm(
                self.request.POST,
                prefix='tarefa'
            )
        else:
            context['processo_form'] = ProcessoForm(
                prefix='processo',
                initial=session_data['processo_data']
            )
            context['tarefa_form'] = TarefaForm(prefix='tarefa')

        # Adiciona metadados ao contexto
        context.update({
            'current_step': session_data['current_step'],
            'cliente_id': session_data['cliente_id'],
            'processo_id': session_data['processo_id'],
            'is_update': bool(self.kwargs.get('pk'))
        })
        
        return context

    def post(self, request, *args, **kwargs):
        """Processa requisições POST normais e AJAX"""
        self.object = None
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.handle_ajax_request(request)
            
        # Processamento tradicional (não-AJAX)
        form = self.get_form()
        processo_form = ProcessoForm(request.POST, prefix='processo')
        tarefa_form = TarefaForm(request.POST, prefix='tarefa')

        if all([form.is_valid(), processo_form.is_valid(), tarefa_form.is_valid()]):
            return self.form_valid(form, processo_form, tarefa_form)
        return self.form_invalid(form, processo_form, tarefa_form)
        
    def handle_ajax_request(self, request):
        """Processa requisições AJAX em etapas"""
        etapa = request.POST.get('etapa')
        
        # Mapeamento de etapas para métodos handlers
        handlers = {
            'cliente': self.process_cliente_step,
            'processo': self.process_processo_step,
            'tarefa': self.process_tarefa_step
        }
        
        if etapa not in handlers:
            return self.json_error_response(
                {'etapa': ['Etapa inválida']},
                status=400
            )
            
        try:
            return handlers[etapa](request)
        except Exception as e:
            return self.json_error_response(
                {'server': [str(e)]},
                status=500
            )
    
    def process_cliente_step(self, request):
        """Processa a etapa do formulário de cliente"""
        form = self.get_form()
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    cliente = form.save(commit=False)
                    cliente.created_by = request.user
                    cliente.save()
                    
                    # Persiste dados na sessão
                    self.persist_step_data(
                        request,
                        step='cliente',
                        form_data=form.cleaned_data,
                        model_id=cliente.id
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'cliente_id': cliente.id,
                        'next_etapa': 'processo',
                        'message': 'Dados do cliente salvos com sucesso!'
                    })
            except Exception as e:
                return self.json_error_response(
                    {'database': ['Erro ao salvar cliente: ' + str(e)]},
                    status=500
                )
        return self.json_error_response(form.errors)
    
    def process_processo_step(self, request):
        """Processa a etapa do formulário de processo"""
        cliente_id = self.get_from_session(request, 'cliente_id')
        if not cliente_id:
            return self.json_error_response(
                {'cliente': ['Sessão expirada ou cliente não criado']},
                status=400
            )
            
        form = ProcessoForm(request.POST, prefix='processo')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    processo = form.save(commit=False)
                    processo.cliente_id = cliente_id
                    processo.created_by = request.user
                    processo.save()
                    form.save_m2m()  # Para campos many-to-many
                    
                    # Persiste dados na sessão
                    self.persist_step_data(
                        request,
                        step='processo',
                        form_data=form.cleaned_data,
                        model_id=processo.id
                    )
                    
                    return JsonResponse({
                        'success': True,
                        'processo_id': processo.id,
                        'next_etapa': 'tarefa',
                        'message': 'Dados do processo salvos com sucesso!'
                    })
            except Exception as e:
                return self.json_error_response(
                    {'database': ['Erro ao salvar processo: ' + str(e)]},
                    status=500
                )
        return self.json_error_response(form.errors)
    
    def process_tarefa_step(self, request):
        """Processa a etapa do formulário de tarefa"""
        processo_id = self.get_from_session(request, 'processo_id')
        if not processo_id:
            return self.json_error_response(
                {'processo': ['Sessão expirada ou processo não criado']},
                status=400
            )
            
        form = TarefaForm(request.POST, prefix='tarefa')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    tarefa = form.save(commit=False)
                    tarefa.processo_id = processo_id
                    tarefa.created_by = request.user
                    tarefa.save()
                    form.save_m2m()  # Para campos many-to-many
                    
                    # Limpa a sessão após conclusão
                    self.clear_session_data()
                    
                    return JsonResponse({
                        'success': True,
                        'redirect_url': str(self.get_success_url()),
                        'message': 'Tarefa salva com sucesso!'
                    })
            except Exception as e:
                return self.json_error_response(
                    {'database': ['Erro ao salvar tarefa: ' + str(e)]},
                    status=500
                )
        return self.json_error_response(form.errors)

    def form_valid(self, form, processo_form, tarefa_form):
        """Processa o salvamento tradicional (não-AJAX)"""
        try:
            with transaction.atomic():
                # Salva cliente
                cliente = form.save(commit=False)
                cliente.created_by = self.request.user
                cliente.save()
                
                # Salva processo
                processo = processo_form.save(commit=False)
                processo.cliente = cliente
                processo.created_by = self.request.user
                processo.save()
                processo_form.save_m2m()
                
                # Salva tarefa
                tarefa = tarefa_form.save(commit=False)
                tarefa.processo = processo
                tarefa.created_by = self.request.user
                tarefa.save()
                tarefa_form.save_m2m()
                
                messages.success(self.request, 'Cadastro realizado com sucesso!')
                return redirect(self.get_success_url())
                
        except Exception as e:
            messages.error(self.request, f'Erro ao salvar: {str(e)}')
            return self.form_invalid(form, processo_form, tarefa_form)

    def form_invalid(self, form, processo_form, tarefa_form):
        """Trata forms inválidos no modo tradicional"""
        # Coleta todos os erros
        errors = []
        
        for field, field_errors in form.errors.items():
            errors.append(f'Cliente - {field}: {", ".join(field_errors)}')
            
        for field, field_errors in processo_form.errors.items():
            errors.append(f'Processo - {field}: {", ".join(field_errors)}')
            
        for field, field_errors in tarefa_form.errors.items():
            errors.append(f'Tarefa - {field}: {", ".join(field_errors)}')
        
        # Exibe os erros
        for error in errors:
            messages.error(self.request, error)

        return self.render_to_response(
            self.get_context_data(
                form=form,
                processo_form=processo_form,
                tarefa_form=tarefa_form
            )
        )

    # Métodos auxiliares
    def persist_step_data(self, request, step, form_data=None, model_id=None):
        """Armazena dados da etapa atual na sessão"""
        if form_data:
            request.session[self.SESSION_KEYS[f'{step}_data']] = form_data
        if model_id:
            request.session[self.SESSION_KEYS[f'{step}_id']] = model_id
        
        request.session[self.SESSION_KEYS['current_step']] = step
        request.session.modified = True

    def get_from_session(self, request, key):
        """Obtém valor da sessão com verificação de existência"""
        session_key = self.SESSION_KEYS.get(key)
        return request.session.get(session_key) if session_key else None

    def clear_session_data(self):
        """Limpa todos os dados do wizard da sessão"""
        for key in self.SESSION_KEYS.values():
            if key in self.request.session:
                del self.request.session[key]
        self.request.session.modified = True

    def json_error_response(self, errors, status=400):
        """Retorna erros de validação formatados"""
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=status)
                            
# CadastroDeleteView
class CadastroDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente  # Define o modelo que será utilizado
    template_name = 'cadastro/delete.html'  # Define o template que será renderizado
    success_url = reverse_lazy('cadastro:list')  # Define a URL de redirecionamento após o sucesso

# CadastroDetailView
class CadastroDetailView(LoginRequiredMixin, DetailView):
    model = Cliente  # Define o modelo que será utilizado
    template_name = 'cadastro/detail.html'  # Define o template que será renderizado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        context["processos"] = Processo.objects.filter(cliente=cliente)
        context["tarefas"] = Tarefa.objects.filter(processo__cliente=cliente)
        return context

# CadastroUpdateView
class CadastroUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cadastro/create.html"
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("cadastro:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.object
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(processo=processo).first() if processo else None

        if self.request.POST:
            context['processo_form'] = ProcessoForm(
                self.request.POST, 
                instance=processo
            )
            context['tarefa_form'] = TarefaForm(
                self.request.POST,
                instance=tarefa
            )
        else:
            context['processo_form'] = ProcessoForm(instance=processo)
            context['tarefa_form'] = TarefaForm(instance=tarefa)
        
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        
        # Verifica se é AJAX
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.handle_ajax_request(request)
            
        return super().post(request, *args, **kwargs)

    def handle_ajax_request(self, request):
        etapa = request.POST.get('etapa')
        cliente = self.object
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(processo=processo).first() if processo else None

        try:
            if etapa == 'cliente':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                    return JsonResponse({
                        'success': True,
                        'cliente_id': cliente.id,
                        'next_etapa': 'processo'
                    })
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)

            elif etapa == 'processo':
                processo_form = ProcessoForm(
                    request.POST, 
                    instance=processo
                ) if processo else ProcessoForm(request.POST)
                
                if processo_form.is_valid():
                    processo = processo_form.save(commit=False)
                    processo.cliente = cliente
                    processo.save()
                    return JsonResponse({
                        'success': True,
                        'processo_id': processo.id,
                        'next_etapa': 'tarefa'
                    })
                return JsonResponse({
                    'success': False,
                    'errors': processo_form.errors
                }, status=400)

            elif etapa == 'tarefa':
                if not processo:
                    return JsonResponse({
                        'success': False,
                        'errors': {'processo': ['Processo não encontrado']}
                    }, status=400)
                
                tarefa_form = TarefaForm(
                    request.POST,
                    instance=tarefa
                ) if tarefa else TarefaForm(request.POST)
                
                if tarefa_form.is_valid():
                    tarefa = tarefa_form.save(commit=False)
                    tarefa.processo = processo
                    tarefa.save()
                    return JsonResponse({
                        'success': True,
                        'redirect_url': self.get_success_url()
                    })
                return JsonResponse({
                    'success': False,
                    'errors': tarefa_form.errors
                }, status=400)

        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': {'server': [str(e)]}
            }, status=500)

    def form_valid(self, form):
        context = self.get_context_data()
        processo_form = context['processo_form']
        tarefa_form = context['tarefa_form']

        try:
            with transaction.atomic():
                cliente = form.save()
                
                if processo_form.is_valid():
                    processo = processo_form.save(commit=False)
                    processo.cliente = cliente
                    processo.save()
                    
                    if tarefa_form.is_valid() and tarefa_form.has_changed():
                        tarefa = tarefa_form.save(commit=False)
                        tarefa.processo = processo
                        tarefa.save()
                
                messages.success(self.request, 'Cadastro atualizado com sucesso!')
                return redirect(self.get_success_url())
                
        except Exception as e:
            messages.error(self.request, f'Erro ao atualizar: {str(e)}')
            return self.form_invalid(form)
        
# CadastroListView
class CadastroListView(LoginRequiredMixin, ListView):
    template_name = 'cadastro/list.html'
    context_object_name = 'clientes'
    model = Cliente

    def get_queryset(self):
        return Cliente.objects.prefetch_related(
            'processos__tarefas'  # tarefas: reverse FK (prefetch)
        ).select_related(
            # parceiro: FK direta no Processo, acessado via select_related
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for cliente in context['clientes']:
            parceiros_set = set()
            for processo in cliente.processos.all():
                if processo.parceiro:  # evita erro se for null
                    parceiros_set.add(processo.parceiro.parceiro)  # campo nome
            cliente.parceiros_unicos = list(parceiros_set)

        return context