from django import forms
from django.contrib.auth import get_user_model

from clientes.widgets import DatePickerInput
from .models import Processo, Tarefa

User = get_user_model()

class TarefaForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=Tarefa.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status da Tarefa"
    )
    
    processo = forms.ModelChoiceField(
        queryset=Processo.objects.all(),
        required=False,
        label="Processo",
        widget=forms.HiddenInput()
    )
    
    # Adicione um campo para selecionar múltiplos responsáveis
    responsaveis = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Responsáveis",
        widget=forms.Select(attrs={'class': 'form-control'})
        
    )

    class Meta:
        model = Tarefa
        fields = '__all__'
        widgets = {
            'tarefa': forms.TextInput(attrs={'class': 'form-control'}),
            'data': DatePickerInput(attrs={'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'prazo_fatal': DatePickerInput(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_tarefa': forms.Textarea(attrs={'class': 'form-control'}),
            'importante': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'futura': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'retroativa': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'privada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
    def clean(self):
        cleaned_data = super().clean()

        # Apenas se quiser garantir booleanos coerentes
        checkbox_fields = ['importante', 'urgente', 'futura', 'retroativa', 'privada']
        for field in checkbox_fields:
            cleaned_data[field] = bool(cleaned_data.get(field, False))

        return cleaned_data
        