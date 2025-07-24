from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from processos.models import Processo
from .forms import ClienteForm
from .models import Cliente
import imghdr
import base64
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages


class ClienteListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Cliente
    context_object_name = 'clientes'
    template_name = 'cliente_list.html'


# class ClienteCreateView(LoginRequiredMixin, CreateView):
#     login_url = reverse_lazy('login')
#     model = Cliente
#     form_class = ClienteForm
#     template_name = 'cliente_form.html'
#     success_url = reverse_lazy('clientes:list')

#     def form_valid(self, form):
#         with transaction.atomic():
#             foto_base64 = self.request.POST.get('foto')
#             if foto_base64:
#                 try:
#                     format, imgstr = foto_base64.split(';base64,')
#                     ext = format.split('/')[-1]
#                     img_data = base64.b64decode(imgstr)
                    
#                     # Verifica se o formato da imagem é válido
#                     img_type = imghdr.what(None, img_data)
#                     if img_type:
#                         ext = img_type  # Ajusta a extensão para o tipo real da imagem
#                         file_name = f'cliente_{self.request.user.id}.{ext}'
#                         image_file = SimpleUploadedFile(file_name, img_data, content_type=f'image/{ext}')
#                         form.instance.foto = image_file
#                     else:
#                         messages.error(self.request, 'Formato de imagem inválido.')
#                         return self.form_invalid(form)

#                 except Exception as e:
#                     messages.error(self.request, f'Erro ao processar imagem: {str(e)}')
#                     return self.form_invalid(form)

#             response = super().form_valid(form)
#             messages.success(self.request, 'Cliente cadastrado com sucesso!')
#             return response


class ClienteDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('login')
    model = Cliente
    context_object_name = 'cliente'
    template_name = 'clientes/cliente_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        context['processos_relacionados'] = Processo.objects.filter(cliente=cliente)
        return context


class ClienteUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_form.html'
    success_url = reverse_lazy('clientes:list')

    def form_valid(self, form):
        with transaction.atomic():
            foto_base64 = self.request.POST.get('foto')
            if foto_base64:
                format, imgstr = foto_base64.split(';base64,')
                ext = format.split('/')[-1]
                data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                form.instance.foto = data
            # return super().form_valid(form)
            response = super().form_valid(form)
            messages.success(self.request, 'Cliente atualizado com sucesso!')
            return response


class ClienteDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Cliente
    context_object_name = 'cliente'
    template_name = 'cliente_confirm_delete.html'
    success_url = reverse_lazy('clientes:list')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Cliente deletado com sucesso!')
        return redirect(success_url)

