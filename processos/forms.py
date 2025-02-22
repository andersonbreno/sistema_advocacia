from django import forms
from .models import Cliente, Processo, Parceiro, Advogado

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
            'numero_processo': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'fase_processo': forms.Select(attrs={'class': 'form-control'}),
            'fechou_contrato': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_contrato': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
            'prioritario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'arquivado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'pendencia': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean(self):
        super().clean()
        return self.cleaned_data
