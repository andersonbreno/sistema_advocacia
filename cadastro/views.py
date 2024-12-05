from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from clientes.forms import ClienteForm
from processos.forms import ProcessoForm
from parceiros.forms import ParceirosForm
from clientes.models import Cliente
from processos.models import Processo
from parceiros.models import Parceiros

class CadastroView(View):
    template_name = 'cadastro.html'

    def get_objects(self, cliente_id, processo_id, parceiro_id):
        """Obtém as instâncias dos modelos ou retorna None se o ID não for fornecido."""
        cliente = get_object_or_404(Cliente, id=cliente_id) if cliente_id else None
        processo = get_object_or_404(Processo, id=processo_id) if processo_id else None
        parceiro = get_object_or_404(Parceiros, id=parceiro_id) if parceiro_id else None
        return cliente, processo, parceiro

    def get_forms(self, cliente=None, processo=None, parceiro=None, data=None):
        """Instancia os formulários com ou sem dados."""
        cliente_form = ClienteForm(data, instance=cliente)
        processo_form = ProcessoForm(data, instance=processo)
        parceiro_form = ParceirosForm(data, instance=parceiro)
        return cliente_form, processo_form, parceiro_form

    def get(self, request, *args, **kwargs):
        """Método para lidar com requisições GET."""
        cliente, processo, parceiro = self.get_objects(
            kwargs.get('cliente_id'), kwargs.get('processo_id'), kwargs.get('parceiro_id')
        )
        cliente_form, processo_form, parceiro_form = self.get_forms(
            cliente=cliente, processo=processo, parceiro=parceiro
        )
        return render(request, self.template_name, {
            'cliente_form': cliente_form,
            'processo_form': processo_form,
            'parceiro_form': parceiro_form,
        })

    def post(self, request, *args, **kwargs):
        """Método para lidar com requisições POST."""
        cliente, processo, parceiro = self.get_objects(
            kwargs.get('cliente_id'), kwargs.get('processo_id'), kwargs.get('parceiro_id')
        )
        cliente_form, processo_form, parceiro_form = self.get_forms(
            cliente=cliente, processo=processo, parceiro=parceiro, data=request.POST
        )

        if cliente_form.is_valid() and processo_form.is_valid() and parceiro_form.is_valid():
            cliente_form.save()
            processo_form.save()
            parceiro_form.save()
            return redirect('alguma_url')  # Substitua 'alguma_url' pela URL de destino.

        # Caso algum formulário seja inválido, renderiza novamente a página com erros.
        return render(request, self.template_name, {
            'cliente_form': cliente_form,
            'processo_form': processo_form,
            'parceiro_form': parceiro_form,
        })

