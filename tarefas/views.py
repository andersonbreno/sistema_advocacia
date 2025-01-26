from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Tarefa
from .forms import TarefaForm


class TarefaListView(ListView):
    model = Tarefa
    context_object_name = 'tarefas'
    template_name = 'tarefa_list.html'    

class TarefaCreateView(CreateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = 'tarefa_form.html'
    success_url = reverse_lazy('tarefas:list')

    def form_valid(self, form):
        
        response = super().form_valid(form)
        messages.success(self.request, 'Tarefa cadastrada com sucesso!')
        return response
    
class TarefaDetailView(DetailView):
    model = Tarefa
    context_object_name = 'tarefa'
    template_name = 'tarefa_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tarefa = context['tarefa']
        processo = tarefa.numero_processo

        tarefas_relacionandas = Tarefa.objects.filter(numero_processo=processo)
        context['tarefas_relacionadas'] = tarefas_relacionandas

class TarefaUpdateView(UpdateView):
    model = Tarefa
    form_class = TarefaForm 
    context_object_name = 'tarefa'
    template_name = 'tarefa_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success_url'] = reverse_lazy('tarefas:list') 
        return context

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Tarefa atualizada com sucesso!')
        return response

class TarefaDeleteView(DeleteView):
    model = Tarefa
    context_object_name = 'tarefa'
    template_name = 'tarefa_confirm_delete.html'
    success_url = reverse_lazy('tarefas:list')

    def delete(self):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Tarefa deletada com sucesso!')

        return redirect(success_url)