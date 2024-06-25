from django.db import models
# from .validators import validar_cep, validar_telefone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
# from cpf_field.models import CPFField

class EstadoCivil(models.TextChoices):
    SOLTEIRO = 'Solteiro(a)', 'Solteiro(a)'
    CASADO = 'Casado(a)', 'Casado(a)'
    DIVORCIADO = 'Divorciado(a)', 'Divorciado(a)'
    VIUVO = 'Viúvo(a)', 'Viúvo(a)'

class VirouCliente(models.TextChoices):
    SIM = 'Sim', 'Sim'
    NAO = 'Não', 'Não'
    PENDENTE = 'Pendente', 'Pendente'
    EM_PROSPECCAO = 'Em prospecção', 'Em prospecção'

class Cliente(models.Model):
    nome = models.CharField(max_length=150)
    # cpf = CPFField('cpf', unique=True)
    data_de_nascimento = models.DateField(blank=True, null=True)
    estado_civil = models.CharField(max_length=20, choices=EstadoCivil.choices, blank=True, null=True)
    profissao = models.CharField(max_length=80, verbose_name='Profissão')
    virou_cliente = models.CharField(max_length=20, choices=VirouCliente.choices, blank=False, null=False)
    cadastrado_advbox = models.BooleanField(default=False)
    cadastrado_planilha = models.BooleanField(default=False)
    justificativa = models.TextField(blank=True)
    descricao = models.TextField(blank=True, verbose_name='Descrição')
    foto = models.ImageField(upload_to='fotos_clientes/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    # Endereço
    cep = models.CharField(max_length=10, blank=True)
    rua = models.CharField(max_length=255, blank=True)
    numero = models.CharField(max_length=10, verbose_name='Número', blank=True)
    complemento = models.CharField(max_length=150, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=2, blank=True)
    
    # Contato
    email = models.EmailField(blank=True)
    telefone = models.CharField(max_length=15, verbose_name='Telefone', blank=True)
    whatsapp = models.BooleanField(default=False)

    def clean(self):
        if not self.cadastrado_planilha and not self.justificativa:
            raise ValidationError({'justificativa': 'Justificativa é necessária se o cliente não está cadastrado na planilha de atendimentos.'})
        
    def __str__(self):
        return self.nome
