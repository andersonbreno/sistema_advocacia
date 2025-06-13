# Importações necessárias para o funcionamento das views
from django.urls import reverse_lazy
from django.views.generic import ListView, UpdateView, DetailView, DeleteView, CreateView
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction


# Importações dos modelos
from clientes.models import Cliente
from processos.models import Processo
from tarefas.models import Tarefa


# Importações dos formulários
from clientes.forms import ClienteForm
from processos.forms import ProcessoForm
from tarefas.forms import TarefaForm

# CadastroCreateView
class CadastroCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "cadastro/create.html"
    success_url = reverse_lazy("cadastro:list")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Inicializa forms
        if self.request.POST:
            context['processo_form'] = ProcessoForm(
                self.request.POST,
                prefix='processo'
            )
            context['tarefa_form'] = TarefaForm(
                self.request.POST,
                prefix='tarefa'
            )
        else:
            context['processo_form'] = ProcessoForm(prefix='processo')
            context['tarefa_form'] = TarefaForm(prefix='tarefa')

        # Adiciona IDs ao contexto se existirem
        if 'cliente_id' in self.request.session:
            context['cliente_id'] = self.request.session['cliente_id']
        if 'processo_id' in self.request.session:
            context['processo_id'] = self.request.session['processo_id']
        
        return context

    def post(self, request, *args, **kwargs):
        etapa = request.POST.get('etapa')
        
        if etapa == 'cliente':
            return self.process_cliente_step(request)
        elif etapa == 'processo':
            return self.process_processo_step(request)
        elif etapa == 'tarefa':
            return self.process_tarefa_step(request)
        else:
            return self.process_all_steps(request)
    
    def process_cliente_step(self, request):
        form = self.get_form()
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    cliente = form.save(commit=False)
                    cliente.created_by = request.user
                    cliente.save()
                    
                    request.session['cliente_id'] = cliente.id
                    request.session.modified = True
                    
                    messages.success(request, 'Dados do cliente salvos com sucesso!')
                    return redirect('cadastro:create')
            except Exception as e:
                messages.error(request, f'Erro ao salvar cliente: {str(e)}')
        else:
            self.mark_invalid_fields(form)
            self.show_form_errors(request, form.errors, 'Cliente')
        
        return self.render_to_response(self.get_context_data(form=form))

    def process_processo_step(self, request):
        cliente_id = request.session.get('cliente_id')
        if not cliente_id:
            messages.error(request, 'Cliente não encontrado. Por favor, preencha os dados do cliente primeiro.')
            return redirect('cadastro:create')
            
        form = ProcessoForm(request.POST, prefix='processo')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    processo = form.save(commit=False)
                    processo.cliente_id = cliente_id
                    processo.created_by = request.user
                    processo.save()
                    form.save_m2m()
                    
                    request.session['processo_id'] = processo.id
                    request.session.modified = True
                    
                    messages.success(request, 'Dados do processo salvos com sucesso!')
                    return redirect('cadastro:create')
            except Exception as e:
                messages.error(request, f'Erro ao salvar processo: {str(e)}')
        else:
            self.mark_invalid_fields(form)
            self.show_form_errors(request, form.errors, 'Processo')
        
        context = self.get_context_data()
        context['processo_form'] = form
        return self.render_to_response(context)

    def process_tarefa_step(self, request):
        processo_id = request.session.get('processo_id')
        if not processo_id:
            messages.error(request, 'Processo não encontrado. Por favor, preencha os dados do processo primeiro.')
            return redirect('cadastro:create')
            
        form = TarefaForm(request.POST, prefix='tarefa')
        
        if form.is_valid():
            try:
                with transaction.atomic():
                    tarefa = form.save(commit=False)
                    tarefa.processo_id = processo_id
                    tarefa.created_by = request.user
                    tarefa.save()
                    form.save_m2m()
                    
                    if 'cliente_id' in request.session:
                        del request.session['cliente_id']
                    if 'processo_id' in request.session:
                        del request.session['processo_id']
                    
                    messages.success(request, 'Tarefa salva com sucesso!')
                    return redirect(self.get_success_url())
            except Exception as e:
                messages.error(request, f'Erro ao salvar tarefa: {str(e)}')
        else:
            self.mark_invalid_fields(form)
            self.show_form_errors(request, form.errors, 'Tarefa')
        
        context = self.get_context_data()
        context['tarefa_form'] = form
        return self.render_to_response(context)

    def mark_invalid_fields(self, form):
        """Adiciona classes CSS aos campos inválidos"""
        for field_name, errors in form.errors.items():
            if field_name in form.fields:
                field = form[field_name]
                css_classes = field.field.widget.attrs.get('class', '')
                if 'is-invalid' not in css_classes:
                    field.field.widget.attrs['class'] = css_classes + ' is-invalid'

    def show_form_errors(self, request, errors, form_name):
        """Exibe erros de validação do formulário"""
        for field, field_errors in errors.items():
            # Remove o prefixo do campo para exibição
            clean_field = field.replace(f'{form_name.lower()}-', '')
            for error in field_errors:
                messages.error(request, f'{form_name} - {clean_field}: {error}')

    def form_invalid(self, form, processo_form, tarefa_form):
        """Trata forms inválidos no modo tradicional"""
        self.mark_invalid_fields(form)
        self.mark_invalid_fields(processo_form)
        self.mark_invalid_fields(tarefa_form)
        
        self.show_form_errors(self.request, form.errors, 'Cliente')
        self.show_form_errors(self.request, processo_form.errors, 'Processo')
        self.show_form_errors(self.request, tarefa_form.errors, 'Tarefa')

        return self.render_to_response(
            self.get_context_data(
                form=form,
                processo_form=processo_form,
                tarefa_form=tarefa_form
            )
        )
                                    
# CadastroDeleteView
class CadastroDeleteView(LoginRequiredMixin, DeleteView):
    model = Cliente  # Define o modelo que será utilizado
    template_name = 'cadastro/delete.html'  # Define o template que será renderizado
    success_url = reverse_lazy('cadastro:list')  # Define a URL de redirecionamento após o sucesso

# CadastroDetailView
class CadastroDetailView(LoginRequiredMixin, DetailView):
    model = Cliente  # Define o modelo que será utilizado
    template_name = 'cadastro/detail.html'  # Define o template que será renderizado

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = self.get_object()
        context["processos"] = Processo.objects.filter(cliente=cliente)
        context["tarefas"] = Tarefa.objects.filter(processo__cliente=cliente)
        return context
       
# CadastroListView
class CadastroListView(LoginRequiredMixin, ListView):
    template_name = 'cadastro/list.html'
    context_object_name = 'clientes'
    model = Cliente

    def get_queryset(self):
        return Cliente.objects.prefetch_related(
            'processos__tarefas'  # tarefas: reverse FK (prefetch)
        ).select_related(
            # parceiro: FK direta no Processo, acessado via select_related
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for cliente in context['clientes']:
            parceiros_set = set()
            for processo in cliente.processos.all():
                if processo.parceiro:  # evita erro se for null
                    parceiros_set.add(processo.parceiro.parceiro)  # campo nome
            cliente.parceiros_unicos = list(parceiros_set)

        return context