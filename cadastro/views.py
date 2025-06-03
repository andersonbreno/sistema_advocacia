# Importações necessárias para o funcionamento das views
from django.db.models import Count  
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
    model = Cliente
    form_class = ClienteForm
    template_name = "cadastro/create.html"
    success_url = reverse_lazy("cadastro:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['processo_form'] = ProcessoForm(self.request.POST)
            context['tarefa_form'] = TarefaForm(self.request.POST)
        else:
            context['processo_form'] = ProcessoForm()
            context['tarefa_form'] = TarefaForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        
        # Verifica se é uma requisição AJAX para salvar em etapas
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return self.handle_ajax_request(request)
            
        # Se não for AJAX, mantém o comportamento original
        form = self.get_form()
        processo_form = ProcessoForm(self.request.POST)
        tarefa_form = TarefaForm(self.request.POST)

        if form.is_valid() and processo_form.is_valid() and tarefa_form.is_valid():
            return self.form_valid(form, processo_form, tarefa_form)
        return self.form_invalid(form, processo_form, tarefa_form)
        
    def handle_ajax_request(self, request):
        etapa = request.POST.get('etapa')
        form_data = {
            'cliente': self.get_form(),
            'processo': ProcessoForm(request.POST),
            'tarefa': TarefaForm(request.POST)
        }
        
        try:
            if etapa == 'cliente':
                form = form_data['cliente']
                if form.is_valid():
                    cliente = form.save()
                    return JsonResponse({
                        'success': True,
                        'cliente_id': cliente.id,
                        'next_etapa': 'processo',
                        'message': 'Dados do cliente salvos com sucesso!'
                    })
                return self.json_error_response(form.errors)
                    
            elif etapa == 'processo':
                cliente_id = request.POST.get('cliente_id')
                if not cliente_id:
                    return self.json_error_response(
                        {'cliente': ['ID do cliente não fornecido']}, 
                        status=400
                    )
                    
                form = form_data['processo']
                if form.is_valid():
                    processo = form.save(commit=False)
                    processo.cliente_id = cliente_id
                    processo.save()
                    return JsonResponse({
                        'success': True,
                        'processo_id': processo.id,
                        'next_etapa': 'tarefa',
                        'message': 'Dados do processo salvos com sucesso!'
                    })
                return self.json_error_response(form.errors)
                    
            elif etapa == 'tarefa':
                processo_id = request.POST.get('processo_id')
                if not processo_id:
                    return self.json_error_response(
                        {'processo': ['ID do processo não fornecido']}, 
                        status=400
                    )
                    
                form = form_data['tarefa']
                if form.is_valid():
                    tarefa = form.save(commit=False)
                    tarefa.processo_id = processo_id
                    tarefa.save()
                    return JsonResponse({
                        'success': True,
                        'redirect_url': str(self.get_success_url()),
                        'message': 'Tarefa salva com sucesso!'
                    })
                return self.json_error_response(form.errors)
                
        except Exception as e:
            return self.json_error_response(
                {'server': [str(e)]}, 
                status=500
            )

    def json_error_response(self, errors, status=400):
        """Helper para retornar erros formatados"""
        return JsonResponse({
            'success': False,
            'errors': errors
        }, status=status)

    def form_valid(self, form, processo_form, tarefa_form):
        try:
            with transaction.atomic():
                cliente = form.save()
                processo = processo_form.save(commit=False)
                processo.cliente = cliente
                processo.save()
                tarefa = tarefa_form.save(commit=False)
                tarefa.processo = processo
                tarefa.save()

                messages.success(self.request, 'Cadastro realizado com sucesso!')
                return redirect(self.get_success_url())
                
        except Exception as e:
            messages.error(self.request, f'Erro ao salvar: {str(e)}')
            return self.form_invalid(form, processo_form, tarefa_form)

    def form_invalid(self, form, processo_form, tarefa_form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Cliente - {field}: {error}')
        
        for field, errors in processo_form.errors.items():
            for error in errors:
                messages.error(self.request, f'Processo - {field}: {error}')
        
        for field, errors in tarefa_form.errors.items():
            for error in errors:
                messages.error(self.request, f'Tarefa - {field}: {error}')

        return self.render_to_response(
            self.get_context_data(
                form=form,
                processo_form=processo_form,
                tarefa_form=tarefa_form
            )
        )
                    
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