from django.db import models
from clientes.models import Cliente
from parceiros.models import Parceiro

class Advogado(models.Model):
    nome = models.CharField(max_length=255)

    def __str__(self):
        return self.nome
    
class Processo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    parceiro = models.ForeignKey(Parceiro, on_delete=models.CASCADE, null=True)
    advogado = models.ForeignKey(Advogado, on_delete=models.CASCADE, verbose_name='Advogado Responsável')
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    numero_processo = models.IntegerField(verbose_name='Número do Processo', null=True, blank=True)    
    
    class Grupo(models.TextChoices):
        ADMINISTRATIVO = 'ADM', 'Administrativo'
        PREVIDENCIARIO = 'PRE', 'Previdenciário'
        CIVEL = 'CIV', 'Cível'
        DPVAT = 'DPV', 'DPVAT'
        EXERCITO = 'EXE', 'Exército'
        REVISAO_FGTS = 'RF', 'Revisão do FGTS'
        IMPORTADO = 'IMP', 'Importado'
        PASEP = 'PAS', 'PASEP'
        PENAL = 'PEN', 'Penal'
        PENDENCIAS_AJUIZAR = 'PAJ', 'Pendências p/ Ajuizar'
        TRABALHISTA = 'TRA', 'Trabalhista'
        TUST_TUSD = 'TT', 'TUST/TUSD'
        # Adicione mais opções se necessário

    grupo = models.CharField(
        max_length=3,
        choices=Grupo.choices,
        default=Grupo.ADMINISTRATIVO,
        verbose_name='Grupo do Processo'
    )

    class FaseProcesso(models.TextChoices):
        ADMINISTRATIVO = 'AD', 'Administrativo'
        ARQUIVO = 'AR', 'Arquivo'
        CONSULTORIA = 'CO', 'Consultoria'
        INICIAL = 'IN', 'Inicial'
        JUDICIAL = 'JU', 'Judicial'
        NEGOCIACAO = 'NE', 'Negociação'
        PENDENCIAS = 'PE', 'Pendências'
        # Adicione mais fases conforme necessário

    fase_processo = models.CharField(
        max_length=2,
        choices=FaseProcesso.choices,
        default=FaseProcesso.INICIAL,
        verbose_name='Fase do Processo'
    )

    fechou_contrato = models.BooleanField(default=False, verbose_name='Fechou Contrato')
    data_contrato = models.DateField(null=True, blank=True, verbose_name='Data do Contrato')
    prioritario = models.BooleanField(default=False, verbose_name='Prioritário')
    arquivado = models.BooleanField(default=False, verbose_name='Arquivado')
    descricao = models.TextField(blank=True, verbose_name='Descrição')

    class Pendencia(models.TextChoices):
        CNIS = 'CNIS', 'CNIS'
        COMPROVANTE_ENDERECO = 'CE', 'Comprovante de endereço'
        COMPROVANTE_HIPOSSUFICIENCIA = 'CH', 'Comprovante de hipossuficiência'
        CTPS = 'CTPS', 'CTPS'
        DOCS_GRUPO_FAMILIAR = 'DGF', 'Documentos do grupo familiar'
        DOCS_PESSOAIS = 'DP', 'Documentos pessoais'
        LAUDOS_MEDICOS = 'LM', 'Laudos médicos'
        # Adicione mais opções conforme necessário

    pendencia = models.CharField(
        max_length=4,
        choices=Pendencia.choices,
        default=Pendencia.CNIS,
        verbose_name='Pendência'
    )

    def __str__(self):
        return f"{self.cliente.nome} - {self.numero_processo}"
