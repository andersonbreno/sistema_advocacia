from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from processos.models import Processo
from .forms import ParceiroForm
from .models import Parceiros
import base64
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages

class ParceiroListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Parceiros
    context_object_name = 'parceiros'
    template_name = 'parceiros/parceiros_list.html'

class ParceiroCreatView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('logins')
    model = Parceiros
    template_name = 'parceiros/parceiros_form.html'
    success_url = reverse_lazy('parceiros:list')

    def form_valid(self, form):

