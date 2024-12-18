from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.shortcuts import redirect, render
from django.contrib import messages

from clientes.forms import ClienteForm
from processos.forms import ProcessoForm


class CadastroView(TemplateView):
    template_name = "cadastro.html"  # Nome do template
    success_url = reverse_lazy("clientes:list")  # URL para redirecionar após salvar
    cliente_form_class = ClienteForm  # Classe do formulário de cliente
    processo_form_class = ProcessoForm  # Classe do formulário de processo

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context["cliente_form"] = self.cliente_form_class()
            context["processo_form"] = self.processo_form_class()
            context["cliente_nome"] = kwargs.get('cliente_nome', None)
            
            return context       

    def post(self, request, *args, **kwargs):
        # Instanciar o formulário do cliente
        cliente_form = self.cliente_form_class(request.POST, request.FILES)

        if cliente_form.is_valid():  # Primeiro, verifica se o formulário do cliente é válido
            # Salva o cliente
            cliente = cliente_form.save()

            # Instancia o formulário do processo, já associando o cliente salvo
            processo_form = self.processo_form_class(
                request.POST, request.FILES, initial={"cliente": cliente}
            )

            if processo_form.is_valid():  # Valida o formulário do processo
                # Salva o processo associado ao cliente
                processo = processo_form.save(commit=False)
                processo.cliente = cliente  # Garante a associação do cliente
                processo.save()

                # Redireciona para a página de sucesso
                return render(
                    request, "cadastro_sucesso.html", {"success_url": self.success_url}
                )

            # Se o processo não for válido, renderiza novamente
            return render(
                request,
                self.template_name,
                {
                    "cliente_form": cliente_form,
                    "processo_form": processo_form,
                    "cliente_nome": cliente.nome
                },
            )

        # Caso o cliente_form não seja válido, renderiza o template com erros
        return render(
            request,
            self.template_name,
            {
                "cliente_form": cliente_form,
                "processo_form": self.processo_form_class(),
            },
        )