from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic.edit import View

from clientes.forms import ClienteForm
from processos.forms import ProcessoForm

class CadastroView(View):
    template_name = "cadastro.html"  # Substitua pelo nome correto do template

    def get(self, request):
        # Instanciar os formulários vazios para a exibição inicial
        cliente_form = ClienteForm()
        processo_form = ProcessoForm()
        return render(request, self.template_name, {
            'cliente_form': cliente_form,
            'processo_form': processo_form
        })

    def post(self, request):
        # Processar os formulários enviados
        cliente_form = ClienteForm(request.POST, request.FILES)
        processo_form = ProcessoForm(request.POST, request.FILES)

        if cliente_form.is_valid() and processo_form.is_valid():
            # Salvar os dados do cliente e do processo
            cliente = cliente_form.save()  # Salva e retorna o objeto cliente
            processo = processo_form.save(commit=False)
            processo.cliente = cliente  # Relaciona o processo ao cliente
            processo.save()

            return redirect('clientes:list')  # Substitua pela URL de destino após o cadastro

        # Se houver erros, renderizar o template com os formulários preenchidos
        return render(request, self.template_name, {
            'cliente_form': cliente_form,
            'processo_form': processo_form
        })