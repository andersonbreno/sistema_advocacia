from django import forms
from django.contrib.auth import get_user_model
from datetime import datetime

from clientes.widgets import DatePickerInput
from .models import Processo, Tarefa, PrioridadeTarefa, Status_Tarefa, ModelTarefa


User = get_user_model()

class TarefaForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=Status_Tarefa.choices,  
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status da Tarefa",
        initial=Status_Tarefa.PENDENTE  
    )    
    processo = forms.ModelChoiceField(
        queryset=Processo.objects.all(),
        required=False,
        label="Processo",
        widget=forms.HiddenInput()
    )    
    responsaveis = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=False,
        label="Responsáveis",
        widget=forms.Select(attrs={'class': 'form-control'})
        
    )
    prioridade_tarefa = forms.ChoiceField(
        choices=PrioridadeTarefa.choices,
        required=True,
        label="Tarefa",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tarefa = forms.ModelChoiceField(
        queryset=ModelTarefa.objects.all(),
        required=True,
        label="Tarefas",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tarefa
        fields = '__all__'
        widgets = {            
            'data': DatePickerInput(attrs={'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'prazo_fatal': DatePickerInput(attrs={'class': 'form-control'}),
            'local': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao_tarefa': forms.Textarea(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.initial['data'] = datetime.now().date()
        
        instance = kwargs.get('instance')
        if instance and instance.status == Status_Tarefa.CONCLUIDA:
            for field in self.fields.values():
                field.disabled = True
    
    def clean(self):
        cleaned_data = super().clean()
        processo = cleaned_data.get('processo')
        
        # Se processo foi fornecido no form (não apenas pelo hidden)
        if processo and not isinstance(processo, Processo):
            try:
                cleaned_data['processo'] = Processo.objects.get(pk=processo)
            except (ValueError, Processo.DoesNotExist):
                self.add_error('processo', 'Processo inválido')
        
        return cleaned_data
        
    def clean(self):
        cleaned_data = super().clean()

        # Apenas se quiser garantir booleanos coerentes
        checkbox_fields = ['importante', 'urgente', 'futura', 'retroativa', 'privada']
        for field in checkbox_fields:
            cleaned_data[field] = bool(cleaned_data.get(field, False))

        return cleaned_data
        