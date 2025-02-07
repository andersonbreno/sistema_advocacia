from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ParceiroForm
from .models import Parceiro
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class ParceirosListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Parceiro
    context_object_name = 'parceiros'
    template_name = 'parceiros/parceiros_list.html'

class ParceirosCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Parceiro
    form_class = ParceiroForm
    template_name = 'parceiros/parceiros_form.html'
    success_url = reverse_lazy('parceiros:list')

    def form_valid(self, form):        
        parceiro = form.cleaned_data.get('parceiro')
        if 'invalid' in parceiro:
            form.add_error('Parceiro', 'O parceiro não pode conter "invalid".')
            return self.form_invalid(form)

        return super().form_valid(form)
    
class ParceirosDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Parceiro
    context_object_name = 'parceiro'
    template_name = 'parceiros/parceiros_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        return context

class ParceirosUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Parceiro
    form_class = ParceiroForm
    template_name = 'parceiros/parceiros_form.html'
    success_url = reverse_lazy('parceiros:list')

    def form_valid(self, form):
        messages.success(self.request, 'Parceiro atualizado com sucesso!')
        return super().form_valid(form)

class ParceirosDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Parceiro
    context_object_name = 'parceiros'
    template_name = 'parceiros/parceiros_confirm_delete.html'
    success_url = reverse_lazy('parceiros:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Parceiro excluído com sucesso!')
        return redirect(success_url)
