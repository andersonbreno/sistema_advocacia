from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ParceiroForm
from .models import Parceiros
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class ParceiroListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Parceiros
    context_object_name = 'parceiros'
    template_name = 'parceiros/parceiros_list.html'

class ParceiroCreatView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('logins')
    model = Parceiros
    form_class = ParceiroForm
    template_name = 'parceiros/parceiros_form.html'
    success_url = reverse_lazy('parceiros:list')

class ParceiroDetailView(LoginRequiredMixin, DetailView):    
    login_url = reverse_lazy('logins')
    model = Parceiros
    context_object_name = 'parceiro'
    template_name = 'parceiros/parceiros_detail.html'
    success_url = reverse_lazy('parceiros:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parceiro = self.get_object()
        context['parceiros_relacionados'] = Processo.objects.filter(parceiro=parceiro)
        return context
    
class ParceirosUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Parceiros
    form_class = ParceiroForm
    template_name = 'parceiros/parceiros_form.html'
    success_url = reverse_lazy('parceiros:list')

