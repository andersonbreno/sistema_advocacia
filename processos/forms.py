from django import forms
from .models import Cliente, Processo, Parceiro, Advogado

class ProcessoForm(forms.ModelForm):
    
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=False, label="Cliente")
    parceiro = forms.ModelChoiceField(queryset=Parceiro.objects.all(), required=True, label="Parceiro/Origem")
    advogado = forms.ModelChoiceField(queryset=Advogado.objects.all(), required=True, label="Advogado")

    class Meta:
        model = Processo
        fields = '__all__'  # Garante que todos os campos sejam incluídos
        widgets = {
            'cliente': forms.HiddenInput(),
            'parceiro': forms.TextInput(attrs={'class': 'form-control'}),
            'advogado': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_processo': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'fase_processo': forms.Select(attrs={'class': 'form-control'}),
            'fechou_contrato': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_contrato': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
            'prioritario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'arquivado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'pendencia': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        super().clean()
        return self.cleaned_data
