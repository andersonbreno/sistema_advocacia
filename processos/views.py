from django.shortcuts import render, redirect

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Processo
from .forms import ProcessoForm
from django.contrib import messages

# Implemente as classes ProcessoListView, ProcessoCreateView, ProcessoDetailView, ProcessoUpdateView, ProcessoDeleteView
# Similar ao que foi feito para o app clientes

class ProcessoListView(ListView):
    model = Processo
    context_object_name = 'processos'
    template_name = 'processo/processo_list.html'  # Caminho para seu template de listagem

class ProcessoCreateView(CreateView):
    model = Processo
    form_class = ProcessoForm
    template_name = 'processos/processo_form.html'  # Caminho para seu template de criação
    success_url = reverse_lazy('processos:list')

    def form_valid(self, form):
        # Adicionar lógica adicional aqui, caso necessário.
        # return super().form_valid(form)
        response = super().form_valid(form)
        messages.success(self.request, 'Processo cadastrado com sucesso!')
        return response
    

class ProcessoDetailView(DetailView):
    model = Processo
    context_object_name = 'processo'
    template_name = 'processos/processo_detail.html'  # Caminho para seu template de detalhes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        processo = context['processo']  # Obtém o processo atual do contexto
        cliente = processo.cliente  # Acessa o cliente relacionado ao processo

        processos_relacionados = Processo.objects.filter(cliente=cliente)
        context['processos_relacionados'] = processos_relacionados  # Adiciona ao contexto

        return context

class ProcessoUpdateView(UpdateView):
    model = Processo
    fields = '__all__'
    context_object_name = 'processo'
    template_name = 'processos/processo_form.html'  # Você pode reutilizar o mesmo template de criação para atualização

    def get_success_url(self):
        return reverse_lazy('processos:list')
    
    def form_valid(self, form):
        # Adicionar lógica adicional aqui
        # return super().form_valid(form)
        response = super().form_valid(form)
        messages.success(self.request, 'Processo atualizado com sucesso!')
        return response

class ProcessoDeleteView(DeleteView):
    model = Processo
    context_object_name = 'processo'
    template_name = 'processos/processo_delete.html'  # Caminho para seu template de confirmação de exclusão
    success_url = reverse_lazy('processos:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Processo deletado com sucesso!')
        return redirect(success_url)