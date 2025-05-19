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
            'fechou_contrato': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_contrato': DatePickerInput(attrs={'class': 'form-control'}), 
            'prioritario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'arquivado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao_processo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pendencia': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_numero_processo(self):
        numero_processo = self.cleaned_data.get('numero_processo', '').strip()
        
        if not numero_processo:
            raise ValidationError("O número do processo é obrigatório")
        
        # Remove todos os caracteres não numéricos
        numeros = re.sub(r'[^0-9]', '', numero_processo)
        
        if len(numeros) != 20:
            raise ValidationError("Deve conter 20 dígitos (formato: 0000000-00.0000.0.00.0000)")
        
        # Formata no padrão correto
        formatado = f"{numeros[:7]}-{numeros[7:9]}.{numeros[9:13]}.{numeros[13]}.{numeros[14:16]}.{numeros[16:20]}"
    
        return formatado
    
    def clean(self):
        cleaned_data = super().clean()

        checkbox_fields = ['fechou_contrato', 'prioritario', 'arquivado']
        for field in checkbox_fields:
            cleaned_data[field] = bool(self.data.get(field))

        return cleaned_data