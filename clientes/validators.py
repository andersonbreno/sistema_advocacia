from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from validate_docbr import CPF

def validar_cep(value):
     # Expressão regular para validar o formato do CEP: XX.XXX-XXX
     if not re.match(r'^\d{2}\.\d{3}-\d{3}$', value):
         raise ValidationError("O formato do CEP deve ser 'XX.XXX-XXX'.")

def validar_cpf(value):
     cpf = CPF()
     if not cpf.validate(value):
         raise ValidationError('CPF inválido.')
     return value

# Não está funcionando ainda
# def formatar_cpf(cpf):
#     """Formata uma string CPF que contém apenas dígitos para o formato XXX.XXX.XXX-XX."""
#     return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"

def validar_cpf(value):
     # Verifica o formato do CPF
     if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', value):
         raise ValidationError('O formato do CPF deve ser "XXX.XXX.XXX-XX".')

     # Limpa o CPF removendo pontos e traço
     cpf = re.sub('[^0-9]', '', value)

     # Verifica se o CPF tem 11 dígitos
     if len(cpf) != 11:
         raise ValidationError('CPF deve conter 11 dígitos numéricos.')

     # Verificação dos dígitos verificadores
     for i in range(9, 11):
         valor = sum((int(cpf[num]) * ((i+1) - num) for num in range(0, i)))
         digito = ((valor * 10) % 11) % 10
         if digito != int(cpf[i]):
             raise ValidationError('CPF inválido.')

     return value

validar_telefone = RegexValidator(
     regex=r'^\(\d{2}\)\s\d{4,5}-\d{4}$',
     message="Número de telefone deve estar no formato: '(XX) XXXX-XXXX' ou '(XX) XXXXX-XXXX'."
 )

def validar_telefone(value):
     if not re.match(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', value):
         raise ValidationError("Número de telefone deve estar no formato: '(XX) XXXX-XXXX' ou '(XX) XXXXX-XXXX'.")




