from django.db import models
from django.contrib.auth.models import User
from processos.models import Processo

class ModelTarefa(models.Model):
    tipo_tarefa = models.CharField(max_length=150)
    
    def __str__(self):
        return self.tipo_tarefa

class Status_Tarefa(models.TextChoices):
    PENDENTE = 'Pendente', 'Pendente'
    EM_PROGRESSO = 'Em Progresso', 'Em Progresso'
    CONCLUIDA = 'Concluída', 'Concluída'

class PrioridadeTarefa(models.TextChoices):
    IMPORTANTE = 'Importante', 'Importante'
    URGENTE = 'Urgente', 'Urgente'
    FUTURA = 'Futura', 'Futura'
    RETROATIVA = 'Retroativa', 'Retroativa'
    PRIVADA = 'Privada', 'Privada'
    
class Tarefa(models.Model):
    PENDENTE = 'PENDENTE'
    EM_PROGRESSO = 'EM_PROGRESSO'
    CONCLUIDA = 'CONCLUIDA'
           
    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, null=True, related_name="tarefas")
    responsaveis = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Responsáveis')    
    tarefa = models.ForeignKey(ModelTarefa, on_delete=models.CASCADE, verbose_name='Tarefa')
    
    data = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    prazo_fatal = models.DateField()
    local = models.CharField(max_length=255, null=True, blank=True)
    descricao_tarefa = models.TextField(null=True, blank=True)
    prioridade_tarefa = models.CharField(max_length=50, choices=PrioridadeTarefa.choices, blank=False, null=False)
    status = models.CharField(max_length=20, choices=Status_Tarefa.choices, default=Status_Tarefa.PENDENTE)

    def __str__(self):
        return f"Tarefa para o processo {self.processo} - {self.get_status_display()}"
