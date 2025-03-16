# Importações necessárias para o funcionamento das views
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages

# Importações dos modelos
from clientes.models import Cliente
from processos.models import Processo
from tarefas.models import Tarefa 

# Importações dos formulários
from clientes.forms import ClienteForm
from processos.forms import ProcessoForm
from tarefas.forms import TarefaForm

# CadastroTemplateView
class CadastroTemplateView(TemplateView):
    template_name = "cadastro/create.html"  # Define o template que será renderizado

    def get_context_data(self, **kwargs):
        # Adiciona ao contexto os formulários de Cliente, Processo e Tarefa
        context = super().get_context_data(**kwargs)
        context["cliente_form"] = ClienteForm()
        context["processo_form"] = ProcessoForm()
        context["tarefa_form"] = TarefaForm()
        return context

    def post(self, request, *args, **kwargs):
        cliente_form = ClienteForm(request.POST)
        processo_form = ProcessoForm(request.POST, request.FILES)
        tarefa_form = TarefaForm(request.POST)

        if cliente_form.is_valid() and processo_form.is_valid() and tarefa_form.is_valid():
            with transaction.atomic():
                # Salva o cliente
                cliente = cliente_form.save()

                # Salva o processo associado ao cliente
                processo = processo_form.save(commit=False)
                processo.cliente = cliente
                processo.save()

                # Salva a tarefa associada ao processo e ao cliente
                tarefa = tarefa_form.save(commit=False)
                tarefa.numero_processo = processo  # Define a instância de Processo
                tarefa.cliente = cliente  # Define a instância de Cliente
                tarefa.save()

            messages.success(request, "Cadastro realizado com sucesso!")
            return redirect(reverse_lazy("cadastro:list"))
        else:
            # Se algum formulário não for válido, re-renderiza o template com os erros
            context = self.get_context_data()
            context["cliente_form"] = cliente_form
            context["processo_form"] = processo_form
            context["tarefa_form"] = tarefa_form
            return self.render_to_response(context)

# CadastroDeleteView
class CadastroDeleteView(DeleteView):
    model = Cliente  # Define o modelo que será utilizado
    template_name = 'cadastro/delete.html'  # Define o template que será renderizado
    success_url = reverse_lazy('cadastro:list')  # Define a URL de redirecionamento após o sucesso

# CadastroDetailView
class CadastroDetailView(DetailView):
    model = Cliente  # Define o modelo que será utilizado
    template_name = 'cadastro/detail.html'  # Define o template que será renderizado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        context["processos"] = Processo.objects.filter(cliente=cliente)
        context["tarefas"] = Tarefa.objects.filter(cliente=cliente)
        return context

# CadastroUpdateView
class CadastroUpdateView(UpdateView):
    template_name = "cadastro/update.html"  # Define o template que será renderizado
    model = Cliente  # Define o modelo que será utilizado
    form_class = ClienteForm  # Define o formulário que será utilizado
    success_url = reverse_lazy("cadastro:list")  # Define a URL de redirecionamento após o sucesso

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        cliente = self.get_object()  # Obtém o objeto Cliente que está sendo atualizado

        # Busca os objetos relacionados ou retorna None
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(processo=processo).first() if processo else None

        # Adiciona os formulários ao contexto
        context["cliente_form"] = self.form_class(instance=cliente)
        context["processo_form"] = ProcessoForm(instance=processo) if processo else ProcessoForm()
        context["tarefa_form"] = TarefaForm(instance=tarefa) if tarefa else TarefaForm()
        
        return context

    def post(self, request, *args, **kwargs):
        cliente = self.get_object()  # Obtém o objeto Cliente que está sendo atualizado
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(processo=processo).first() if processo else None

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
class CadastroListView(ListView):
    template_name = 'cadastro/list.html'  # Define o template que será renderizado
    context_object_name = 'clientes'  # Define o nome do objeto no contexto
    model = Cliente  # Define o modelo que será utilizado

    def get_queryset(self):
        # Carrega todos os clientes com seus processos e tarefas
        return Cliente.objects.prefetch_related(
            'processos__tarefas'
        ).all()