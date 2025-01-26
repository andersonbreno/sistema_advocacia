from django.db import models
from django.contrib.auth.models import User
from processos.models import Processo

STATUS_CHOICES = [
    ('pendente', 'Pendente'),
    ('em_progresso', 'Em Progresso'),
    ('concluido', 'Concluído'),
]

class Tarefa(models.Model):
    numero_processo = models.ForeignKey(
        Processo, 
        on_delete=models.CASCADE, 
        verbose_name='Número do Processo', 
        null=True, 
        blank=True
    )
    responsaveis = models.ManyToManyField(User, related_name='tarefas')
    tarefa = models.TextField()
    data = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    prazo_fatal = models.DateField()
    local = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    importante = models.BooleanField(default=False)
    urgente = models.BooleanField(default=False)
    futura = models.BooleanField(default=False)
    retroativa = models.BooleanField(default=False)
    privada = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
    )

    def __str__(self):
        return f"Tarefa para o processo {self.numero_processo} - {self.get_status_display()}"
