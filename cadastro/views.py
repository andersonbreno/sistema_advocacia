from django.views.generic import ListView, UpdateView, DetailView, DeleteView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from itertools import chain

from clientes.models import Cliente
from processos.models import Processo
from tarefas.models import Tarefa 
from parceiros.models import Parceiro

from clientes.forms import ClienteForm
from processos.forms import ProcessoForm
from tarefas.forms import TarefaForm
from parceiros.forms import ParceiroForm 


# CadastroCreateView
class CadastroCreateView(FormView):
    template_name = "cadastro.html"  
    success_url = reverse_lazy("cadastro:list")  
    form_class = ClienteForm  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cliente_form"] = ClienteForm()
        context["processo_form"] = ProcessoForm()
        context["tarefa_form"] = TarefaForm()
        context["parceiro_form"] = ParceiroForm()
        context["cliente_nome"] = kwargs.get('cliente_nome', None)
        return context

    def form_valid(self, form):
        cliente = form.save()  # Salva o cliente
        
        processo_form = ProcessoForm(self.request.POST, self.request.FILES)
        if not processo_form.is_valid():
            return self.render_to_response(self.get_context_data(form=form, processo_form=processo_form))
        
        processo = processo_form.save(commit=False)
        processo.cliente = cliente  # Associa o cliente ao processo
        processo.save()
        
        tarefa_form = TarefaForm(self.request.POST)
        if not tarefa_form.is_valid():
            return self.render_to_response(self.get_context_data(form=form, processo_form=processo_form, tarefa_form=tarefa_form))
        
        tarefa = tarefa_form.save(commit=False)
        tarefa.processo = processo  # Associa a tarefa ao processo
        tarefa.cliente = cliente  # Associa a tarefa ao cliente
        tarefa.save()
        
        return redirect(self.success_url)


# CadastroDeleteView
class CadastroDeleteView(DeleteView):
    model = Cliente
    template_name = 'cadastro_delete.html'
    success_url = reverse_lazy('cadastro:list')


# CadastroDetailView
class CadastroDetailView(DetailView):
    model = Cliente
    template_name = 'cadastro_detail.html'


# CadastroUpdateView
class CadastroUpdateView(UpdateView):
    template_name = "cadastro_update.html"
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("cadastro:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        cliente = self.get_object()

        # Busca os objetos relacionados ou retorna None
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(processo=processo).first() if processo else None
        parceiro = Parceiro.objects.filter(cliente=cliente).first()

        # Adiciona os formulários ao contexto
        context["cliente_form"] = self.form_class(instance=cliente)
        context["processo_form"] = ProcessoForm(instance=processo) if processo else ProcessoForm()
        context["tarefa_form"] = TarefaForm(instance=tarefa) if tarefa else TarefaForm()
        context["parceiro_form"] = ParceiroForm(instance=parceiro) if parceiro else ParceiroForm()
        
        return context

    def post(self, request, *args, **kwargs):
        cliente = self.get_object()
        processo = Processo.objects.filter(cliente=cliente).first()
        tarefa = Tarefa.objects.filter(processo=processo).first() if processo else None
        parceiro = Parceiro.objects.filter(cliente=cliente).first()

        cliente_form = self.form_class(request.POST, request.FILES, instance=cliente)
        processo_form = ProcessoForm(request.POST, request.FILES, instance=processo) if processo else ProcessoForm(request.POST, request.FILES)
        tarefa_form = TarefaForm(request.POST, instance=tarefa) if tarefa else TarefaForm(request.POST)
        parceiro_form = ParceiroForm(request.POST, instance=parceiro) if parceiro else ParceiroForm(request.POST)

        if all([cliente_form.is_valid(), processo_form.is_valid(), tarefa_form.is_valid(), parceiro_form.is_valid()]):
            cliente_form.save()
            processo = processo_form.save(commit=False)
            processo.cliente = cliente
            processo.save()

            tarefa = tarefa_form.save(commit=False)
            tarefa.processo = processo
            tarefa.save()

            parceiro = parceiro_form.save(commit=False)
            parceiro.cliente = cliente
            parceiro.save()

            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(
            cliente_form=cliente_form,
            processo_form=processo_form,
            tarefa_form=tarefa_form,
            parceiro_form=parceiro_form,
        ))


# CadastroListView
class CadastroListView(ListView):
    template_name = 'cadastro_list.html'
    context_object_name = 'clientes'
    model = Cliente

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Carregar dados relacionados de maneira otimizada
        context['clientes'] = Cliente.objects.prefetch_related(
            'processos', 
            'processos__tarefas', 
            'processos__tarefas__parceiros'
        )
        
        return context   