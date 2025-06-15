from django.contrib import admin
from tarefas.models import ModelTarefa

@admin.register(ModelTarefa)
class ModelTarefaAdmin(admin.ModelAdmin):
    list_display = ('tipo_tarefa',)
