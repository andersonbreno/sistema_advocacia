from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re
from validate_docbr import CPF

def validar_cep(value):
    """Valida o formato do CEP (XX.XXX-XXX) e verifica se é válido"""
    if not re.match(r'^\d{2}\.\d{3}-\d{3}$', value):
        raise ValidationError("O formato do CEP deve ser 'XX.XXX-XXX'.")
    
    # Remove formatação para verificar dígitos
    cep_numeros = re.sub(r'[^\d]', '', value)
    
    # Verifica se todos os dígitos não são iguais (ex: 00.000-000)
    if all(c == cep_numeros[0] for c in cep_numeros):
        raise ValidationError("CEP inválido.")

    return value

def validar_cpf(value):
    """Valida o CPF tanto no formato XXX.XXX.XXX-XX quanto em dígitos puros"""
    cpf = CPF()
    
    # Remove formatação para validação
    cpf_limpo = re.sub(r'[^\d]', '', value)
    
    # Verifica se tem 11 dígitos
    if len(cpf_limpo) != 11:
        raise ValidationError('CPF deve conter 11 dígitos.')
    
    # Verifica se todos os dígitos não são iguais
    if all(c == cpf_limpo[0] for c in cpf_limpo):
        raise ValidationError('CPF inválido.')
    
    # Usa a biblioteca validate_docbr para validação dos dígitos
    if not cpf.validate(cpf_limpo):
        raise ValidationError('CPF inválido.')
    
    return value

def formatar_cpf(cpf):
    """Formata uma string CPF que contém apenas dígitos para o formato XXX.XXX.XXX-XX"""
    cpf_limpo = re.sub(r'[^\d]', '', cpf)
    if len(cpf_limpo) != 11:
        return cpf  # Retorna original se não tiver 11 dígitos
    return f"{cpf_limpo[:3]}.{cpf_limpo[3:6]}.{cpf_limpo[6:9]}-{cpf_limpo[9:]}"

def validar_telefone(value):
    """Valida telefone nos formatos (XX) XXXX-XXXX ou (XX) XXXXX-XXXX"""
    if not re.match(r'^\(\d{2}\)\s\d{4,5}-\d{4}$', value):
        raise ValidationError(
            "Número de telefone deve estar no formato: '(XX) XXXX-XXXX' ou '(XX) XXXXX-XXXX'."
        )
    
    # Remove formatação para verificação adicional
    telefone_limpo = re.sub(r'[^\d]', '', value)
    
    # Verifica se o DDD é válido (lista de DDDs brasileiros)
    ddds_validos = [
        11, 12, 13, 14, 15, 16, 17, 18, 19,
        21, 22, 24, 27, 28,
        31, 32, 33, 34, 35, 37, 38,
        41, 42, 43, 44, 45, 46, 47, 48, 49,
        51, 53, 54, 55,
        61, 62, 63, 64, 65, 66, 67, 68, 69,
        71, 73, 74, 75, 77, 79,
        81, 82, 83, 84, 85, 86, 87, 88, 89,
        91, 92, 93, 94, 95, 96, 97, 98, 99
    ]
    
    ddd = int(telefone_limpo[:2])
    if ddd not in ddds_validos:
        raise ValidationError("DDD inválido.")
    
    return value

def formatar_telefone(telefone):
    """Formata um número de telefone para o padrão (XX) XXXX-XXXX ou (XX) XXXXX-XXXX"""
    telefone_limpo = re.sub(r'[^\d]', '', telefone)
    
    if len(telefone_limpo) == 10:  # Telefone fixo
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:6]}-{telefone_limpo[6:]}"
    elif len(telefone_limpo) == 11:  # Celular
        return f"({telefone_limpo[:2]}) {telefone_limpo[2:7]}-{telefone_limpo[7:]}"
    else:
        return telefone  # Retorna original se não puder formatar