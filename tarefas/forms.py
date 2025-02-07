from django import forms
from .models import Tarefa, Processo

class TarefaForm(forms.ModelForm):
    numero_processo = forms.ModelChoiceField(
        queryset=Processo.objects.all(), 
        required=True, 
        label="Número do Processo"
        )

    status = forms.ChoiceField(
        choices=Tarefa.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status da Tarefa"
    )

    class Meta:
        model = Tarefa
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'numero_processo': forms.Select(attrs={'class': 'form-control'}),
            'responsaveis': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tarefa': forms.Textarea(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'prazo_fatal': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'futura': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retroativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

