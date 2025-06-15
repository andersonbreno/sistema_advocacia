from django import forms
from django.core.exceptions import ValidationError
from clientes.widgets import DatePickerInput
from .models import Cliente, Processo, Parceiro, Advogado
import re

class ProcessoForm(forms.ModelForm):
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        required=False,
        label="Cliente",
        widget=forms.HiddenInput()
    )

    parceiro = forms.ModelChoiceField(
        queryset=Parceiro.objects.all(),
        required=True,
        label="Parceiro/Origem",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    advogado = forms.ModelChoiceField(
        queryset=Advogado.objects.all(),
        required=True,
        label="Advogado",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Processo
        fields = '__all__'
        widgets = {
            'numero_processo': forms.TextInput(attrs={'class': 'form-control process-mask'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'fase_processo': forms.Select(attrs={'class': 'form-control'}),
            'fechou_contrato': forms.Select(attrs={'class': 'form-control'}),
            'data_contrato': DatePickerInput(attrs={'class': 'form-control'}), 
            'processo_status':forms.Select(attrs={'class': 'form-control'}),
            'descricao_processo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pendencia': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_numero_processo(self):
        try:
            # Obtém o valor do campo com fallback para string vazia
            numero_processo = self.cleaned_data.get('numero_processo', '')

            # Verifica se o valor é None ou vazio antes de processar
            if numero_processo is None:
                raise ValidationError("O número do processo não pode ser nulo")

            # Converte para string e remove espaços
            numero_processo = str(numero_processo).strip()

            if not numero_processo:
                raise ValidationError("O número do processo é obrigatório")

            # Remove todos os caracteres não numéricos
            numeros = re.sub(r'[^0-9]', '', numero_processo)

            # Validação do comprimento
            if len(numeros) != 20:
                raise ValidationError(
                    "Deve conter exatamente 20 dígitos. "
                    "Formato esperado: 0000000-00.0000.0.00.0000"
                )

            # Formatação no padrão CNJ
            formatado = (
                f"{numeros[:7]}-{numeros[7:9]}."
                f"{numeros[9:13]}.{numeros[13]}."
                f"{numeros[14:16]}.{numeros[16:20]}"
            )

            # Validação adicional do formato (opcional)
            if not re.match(r'^\d{7}-\d{2}\.\d{4}\.\d\.\d{2}\.\d{4}$', formatado):
                raise ValidationError("Formato inválido após validação interna")

            return formatado

        except Exception as e:
            # Captura erros inesperados e fornece feedback mais amigável
            if isinstance(e, ValidationError):
                raise e
            raise ValidationError("Ocorreu um erro ao validar o número do processo") from e
        