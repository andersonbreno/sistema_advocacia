# Importações necessárias para o funcionamento das views
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction


# Importações dos modelos
from clientes.models import Cliente
from processos.models import Processo
from tarefas.models import Tarefa


# Importações dos formulários
from clientes.forms import ClienteForm
from processos.forms import ProcessoForm
from tarefas.forms import TarefaForm

class CadastroCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cadastro/create.html"
    success_url = reverse_lazy("cadastro:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['processo_form'] = ProcessoForm(self.request.POST, self.request.FILES)
            context['tarefa_form'] = TarefaForm(self.request.POST)
        else:
            context['processo_form'] = ProcessoForm()
            context['tarefa_form'] = TarefaForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        processo_form = ProcessoForm(self.request.POST, self.request.FILES)
        tarefa_form = TarefaForm(self.request.POST)

        if form.is_valid() and processo_form.is_valid() and tarefa_form.is_valid():
            return self.form_valid(form, processo_form, tarefa_form)
        else:
            return self.form_invalid(form, processo_form, tarefa_form)

    def form_valid(self, form, processo_form, tarefa_form):
        try:
            with transaction.atomic():
                self.object = form.save()
                processo = processo_form.save(commit=False)
                processo.cliente = self.object
                processo.save()

                tarefa = tarefa_form.save(commit=False)
                tarefa.numero_processo = processo
                tarefa.cliente = self.object  # adicionado
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
        context["tarefas"] = Tarefa.objects.filter(numero_processo__cliente=cliente)
        return context

# CadastroUpdateView
class CadastroUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "cadastro/create.html"  # Define o template que será renderizado
    model = Cliente  # Define o modelo que será utilizado
    form_class = ClienteForm  # Define o formulário que será utilizado
    success_url = reverse_lazy("cadastro:list")  # Define a URL de redirecionamento após o sucesso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        cliente = self.get_object()  # Obtém o objeto Cliente que está sendo atualizado

        # Busca os objetos relacionados ou retorna None
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(numero_processo=processo).first() if processo else None

        # Adiciona os formulários ao contexto
        context["cliente_form"] = self.form_class(instance=cliente)
        context["processo_form"] = ProcessoForm(instance=processo) if processo else ProcessoForm()
        context["tarefa_form"] = TarefaForm(instance=tarefa) if tarefa else TarefaForm()
        
        return context

    def post(self, request, *args, **kwargs):
        cliente = self.get_object()  # Obtém o objeto Cliente que está sendo atualizado
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(numero_processo=processo).first() if processo else None

        # Valida os formulários
        cliente_form = self.form_class(request.POST, request.FILES, instance=cliente)
        processo_form = ProcessoForm(request.POST, request.FILES, instance=processo) if processo else ProcessoForm(request.POST, request.FILES)
        tarefa_form = TarefaForm(request.POST, instance=tarefa) if tarefa else TarefaForm(request.POST)

        # Se todos os formulários forem válidos, salva as alterações
        if all([cliente_form.is_valid(), processo_form.is_valid(), tarefa_form.is_valid()]):
            cliente_form.save()
            processo = processo_form.save(commit=False)
            processo.cliente = cliente
            processo.save()

            tarefa = tarefa_form.save(commit=False)
            tarefa.processo = processo
            tarefa.save()

            return redirect(self.success_url)

        # Se algum formulário não for válido, re-renderiza a página com os erros
        return self.render_to_response(self.get_context_data(
            cliente_form=cliente_form,
            processo_form=processo_form,
            tarefa_form=tarefa_form,
        ))

# CadastroListView
class CadastroListView(LoginRequiredMixin, ListView):
    template_name = 'cadastro/list.html'  # Define o template que será renderizado
    context_object_name = 'clientes'  # Define o nome do objeto no contexto
    model = Cliente  # Define o modelo que será utilizado

    def get_queryset(self):
        # Carrega todos os clientes com seus processos e tarefas
        return Cliente.objects.prefetch_related(
            'processos__tarefas'
        ).all()