from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from .models import Tarefa
from .forms import TarefaForm, Status_Tarefa


class TarefaListView(ListView):
    model = Tarefa
    template_name = 'tarefa_list.html'
    context_object_name = 'tarefas'
    paginate_by = 10


class TarefaDetailView(DetailView):
    model = Tarefa
    template_name = 'tarefa_detail.html'
    context_object_name = 'tarefa'


class TarefaUpdateView(UpdateView):
    model = Tarefa
    form_class = TarefaForm
    template_name = 'tarefa_form.html'
    success_url = reverse_lazy('tarefas:list')

    def form_valid(self, form):
        if self.object.status == Status_Tarefa.CONCLUIDA:
            messages.error(self.request, "Tarefa concluída não pode ser editada.")
            return redirect('tarefas:detail', pk=self.object.pk)

        messages.success(self.request, "Tarefa atualizada com sucesso.")
        return super().form_valid(form)


class TarefaDeleteView(DeleteView):
    model = Tarefa
    template_name = 'tarefa_confirm_delete.html'
    success_url = reverse_lazy('tarefas:list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Tarefa excluída com sucesso.")
        return super().delete(request, *args, **kwargs)


# Duplicar tarefa
def tarefa_duplicar_view(request, pk):
    tarefa = get_object_or_404(Tarefa, pk=pk)

    if tarefa.status != Status_Tarefa.CONCLUIDA:
        messages.error(request, "A tarefa só pode ser duplicada se estiver concluída.")
        return redirect('tarefas:list')

    tarefa.pk = None
    tarefa.save()
    messages.success(request, "Tarefa duplicada com sucesso.")
    return redirect('tarefas:update', pk=tarefa.pk)

