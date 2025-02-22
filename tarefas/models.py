from django.db import models
from django.contrib.auth.models import User
from processos.models import Processo
from clientes.models import Cliente

class Tarefa(models.Model):
    PENDENTE = 'PENDENTE'
    EM_PROGRESSO = 'EM_PROGRESSO'
    CONCLUIDA = 'CONCLUIDA'
           
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True, related_name="tarefas")
    numero_processo = models.ForeignKey(Processo, on_delete=models.CASCADE, null=True, related_name="tarefas")
    
    responsaveis = models.ManyToManyField(User, related_name='tarefas')
    tarefa = models.CharField(max_length=100)
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
    STATUS_CHOICES = [
        (PENDENTE, 'Pendente'),
        (EM_PROGRESSO, 'Em Progresso'),
        (CONCLUIDA, 'Concluída'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pendente',
    )

    def __str__(self):
        return f"Tarefa para o processo {self.numero_processo} - {self.get_status_display()}"
