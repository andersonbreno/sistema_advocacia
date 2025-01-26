from django import forms
from .models import Tarefa, Processo

class TarefaForm(forms.ModelForm):
    numero_processo = forms.ModelChoiceField(queryset=Processo.objects.all(), required=True, label="Número do Processo")

    class Meta:
        model = Tarefa
        fields = '__all__'  # Inclui todos os campos do modelo
        widgets = {
            'numero_processo': forms.Select(attrs={'class': 'form-control'}),
            'data': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'prazo_fatal': forms.DateInput(attrs={'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

