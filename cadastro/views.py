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
        form = self.get_form()
        processo_form = ProcessoForm(self.request.POST or None)
        tarefa_form = TarefaForm(self.request.POST or None)

        # Verifica se é uma requisição AJAX para salvar em etapas
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            etapa = request.POST.get('etapa')
            
            if etapa == 'cliente':
                if form.is_valid():
                    cliente = form.save()
                    self.object = cliente
                    return JsonResponse({
                        'success': True,
                        'cliente_id': cliente.id,
                        'next_etapa': 'processo'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'errors': form.errors
                    })
                    
            elif etapa == 'processo':
                if processo_form.is_valid():
                    processo = processo_form.save(commit=False)
                    processo.cliente_id = request.POST.get('cliente_id')
                    processo.save()
                    self.object = processo 
                    return JsonResponse({
                        'success': True,
                        'processo_id': processo.id,
                        'next_etapa': 'tarefa'
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'errors': processo_form.errors
                    })
                    
            elif etapa == 'tarefa':
                if tarefa_form.is_valid():
                    tarefa = tarefa_form.save(commit=False)
                    tarefa.numero_processo_id = request.POST.get('processo_id')
                    tarefa.save()
                    self.object = tarefa
                    return JsonResponse({
                        'success': True,
                        'redirect_url': self.get_success_url()
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'errors': tarefa_form.errors
                    })

        # Se não for AJAX, mantém o comportamento original
        if form.is_valid():
            return self.form_valid(form, processo_form, tarefa_form)
        else:
            return self.form_invalid(form, processo_form, tarefa_form)
        
    def form_valid(self, form, processo_form, tarefa_form):
        try:
            with transaction.atomic():
                # 1. Salva o cliente primeiro
                cliente = form.save()
                
                # 2. Configura e salva o processo associado ao cliente
                processo = processo_form.save(commit=False)
                processo.cliente = cliente
                
                # Valida o processo com o cliente já definido
                processo_form.instance = processo
                if not processo_form.is_valid():
                    return self.form_invalid(form, processo_form, tarefa_form)
                
                processo.save()
                
                # 3. Configura e salva a tarefa associada ao processo
                tarefa = tarefa_form.save(commit=False)
                tarefa.numero_processo = processo
                tarefa.cliente = cliente
                
                # Valida a tarefa com o processo já definido
                tarefa_form.instance = tarefa
                if not tarefa_form.is_valid():
                    return self.form_invalid(form, processo_form, tarefa_form)
                
                tarefa.save()

                messages.success(self.request, 'Cadastro realizado com sucesso!')
                return redirect(self.get_success_url())
                
        except Exception as e:
            messages.error(self.request, f'Ocorreu um erro ao salvar: {str(e)}')
            return self.form_invalid(form, processo_form, tarefa_form)

    def form_invalid(self, form, processo_form, tarefa_form):
        # Adiciona mensagens de erro específicas para cada formulário
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f'Cliente - {field}: {error}')
        
        if hasattr(processo_form, 'errors'):
            for field, errors in processo_form.errors.items():
                for error in errors:
                    messages.error(self.request, f'Processo - {field}: {error}')
        
        if hasattr(tarefa_form, 'errors'):
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

    def get_object(self, queryset=None):
        """Garante que o objeto seja carregado corretamente"""
        obj = super().get_object(queryset)
        return obj

    def get_context_data(self, **kwargs):
        """Prepara o contexto para o template"""
        context = super().get_context_data(**kwargs)
        cliente = self.object
        
        # Busca objetos relacionados
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(processo=processo).first() if processo else None

        # Inicializa os formulários
        if self.request.POST:
            context['cliente_form'] = self.form_class(
                self.request.POST, 
                self.request.FILES, 
                instance=cliente
            )
            context['processo_form'] = ProcessoForm(
                self.request.POST, 
                instance=processo
            ) if processo else ProcessoForm(self.request.POST)
            context['tarefa_form'] = TarefaForm(
                self.request.POST, 
                instance=tarefa
            ) if tarefa else TarefaForm(self.request.POST)
        else:
            context['cliente_form'] = self.form_class(instance=cliente)
            context['processo_form'] = ProcessoForm(instance=processo) if processo else ProcessoForm()
            context['tarefa_form'] = TarefaForm(instance=tarefa) if tarefa else TarefaForm()
        
        return context

    def post(self, request, *args, **kwargs):
        """Processa o formulário de atualização"""
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """Processa os dados quando todos os formulários são válidos"""
        context = self.get_context_data()
        cliente_form = form
        processo_form = context['processo_form']
        tarefa_form = context['tarefa_form']

        try:
            with transaction.atomic():
                # Salva o cliente
                cliente = cliente_form.save()
                
                # Salva o processo
                processo = processo_form.save(commit=False)
                processo.cliente = cliente
                processo.save()
                
                # Salva a tarefa
                if tarefa_form.has_changed():  # Só salva se houver alterações
                    tarefa = tarefa_form.save(commit=False)
                    tarefa.processo = processo
                    tarefa.save()
                
                messages.success(self.request, 'Cadastro atualizado com sucesso!')
                return redirect(self.get_success_url())
                
        except Exception as e:
            messages.error(self.request, f'Erro ao atualizar: {str(e)}')
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Processa erros de validação"""
        context = self.get_context_data()
        cliente_form = form
        processo_form = context['processo_form']
        tarefa_form = context['tarefa_form']
        
        # Coleta todos os erros
        for field, errors in cliente_form.errors.items():
            for error in errors:
                messages.error(self.request, f'Cliente - {field}: {error}')
        
        if processo_form.errors:
            for field, errors in processo_form.errors.items():
                for error in errors:
                    messages.error(self.request, f'Processo - {field}: {error}')
        
        if tarefa_form.errors:
            for field, errors in tarefa_form.errors.items():
                for error in errors:
                    messages.error(self.request, f'Tarefa - {field}: {error}')

        return self.render_to_response(self.get_context_data(form=form))

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