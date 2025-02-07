from django.views.generic import TemplateView, ListView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render

from clientes.models import Cliente
from processos.models import Processo
from tarefas.models import Tarefa 
from parceiros.models import Parceiro

from clientes.forms import ClienteForm
from processos.forms import ProcessoForm
from tarefas.forms import TarefaForm
from parceiros.forms import ParceiroForm 

# CadastroCreateView
class CadastroCreateView(TemplateView):
    template_name = "cadastro.html"  
    success_url = reverse_lazy("cadastro:list")  
    cliente_form_class = ClienteForm  
    processo_form_class = ProcessoForm  
    tarefa_form_class = TarefaForm  
    parceiro_form_class = ParceiroForm  

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cliente_form"] = self.cliente_form_class()
        context["processo_form"] = self.processo_form_class()
        context["tarefa_form"] = self.tarefa_form_class()
        context["parceiro_form"] = self.parceiro_form_class()
        context["cliente_nome"] = kwargs.get('cliente_nome', None)

        return context

    def post(self, request, *args, **kwargs):
        cliente_form = self.cliente_form_class(request.POST, request.FILES)

        if cliente_form.is_valid():
            cliente = cliente_form.save()
            processo_form = self.processo_form_class(request.POST, request.FILES)

            if processo_form.is_valid():
                processo = processo_form.save(commit=False)
                processo.cliente = cliente
                processo.save()

                tarefa_form = self.tarefa_form_class(request.POST)

                if tarefa_form.is_valid():
                    tarefa = tarefa_form.save(commit=False)
                    tarefa.processo = processo
                    tarefa.save()

                    return render(request, "processo_list.html", {"success_url": self.success_url})

                return render(request, self.template_name, {
                    "cliente_form": cliente_form,
                    "processo_form": processo_form,
                    "tarefa_form": tarefa_form,
                    "cliente_nome": cliente.nome,
                })

            return render(request, self.template_name, {
                "cliente_form": cliente_form,
                "processo_form": processo_form,
                "tarefa_form": self.tarefa_form_class(),
                "cliente_nome": cliente.nome,
            })

        return render(request, self.template_name, {
            "cliente_form": cliente_form,
            "processo_form": self.processo_form_class(),
            "tarefa_form": self.tarefa_form_class(),
        })

# CadastroDeleteView
class CadastroDeleteView(DeleteView):
    model = Cliente
    template_name = 'cadastro_confirm_delete.html'
    success_url = reverse_lazy('cadastro:list')

    def get_object(self, queryset=None):
        return get_object_or_404(Cliente, pk=self.kwargs.get('pk'))

# CadastroDetailView
class CadastroDetailView(DetailView):
    model = Cliente
    template_name = 'cadastro_detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Cliente, pk=self.kwargs.get('pk'))

# CadastroUpdateView
class CadastroUpdateView(UpdateView):
    template_name = "cadastro_update.html"
    model = Cliente
    form_class = ClienteForm
    success_url = reverse_lazy("cadastro:list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        cliente = self.get_object()

        # Buscar os objetos relacionados ou criar um novo, se não existir
        processo, _ = Processo.objects.get_or_create(cliente=cliente)
        tarefa, _ = Tarefa.objects.get_or_create(processo=processo)
        parceiro, _ = Parceiro.objects.get_or_create(parceiro=cliente.nome)

        # Adiciona os formulários ao contexto
        context["cliente_form"] = self.form_class(instance=cliente)
        context["processo_form"] = ProcessoForm(instance=processo)
        context["tarefa_form"] = TarefaForm(instance=tarefa)
        context["parceiro_form"] = ParceiroForm(instance=parceiro)
        
        return context

    def post(self, request, *args, **kwargs):
        cliente = self.get_object()
        processo, _ = Processo.objects.get_or_create(cliente=cliente)
        tarefa, _ = Tarefa.objects.get_or_create(processo=processo)
        parceiro, _ = Parceiro.objects.get_or_create(parceiro=cliente.nome)

        cliente_form = self.form_class(request.POST, request.FILES, instance=cliente)
        processo_form = ProcessoForm(request.POST, request.FILES, instance=processo)
        tarefa_form = TarefaForm(request.POST, instance=tarefa)
        parceiro_form = ParceiroForm(request.POST, instance=parceiro)

        if all ([cliente_form.is_valid(), processo_form.is_valid(), tarefa_form.is_valid(), parceiro_form.is_valid()]):
            cliente_form.save()
            processo_form.save()
            tarefa_form.save()
            parceiro_form.save()
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
    context_object_name = 'cadastros'
    
    def get_queryset(self):
        clientes = Cliente.objects.all()
        processos = Processo.objects.all()
        tarefas = Tarefa.objects.all()
        parceiros = Parceiro.objects.all()
        
        return {
            'clientes': clientes,
            'processos': processos,
            'tarefas': tarefas,
            'parceiros': parceiros,
        }