from django import forms
from .models import Tarefa, Processo

class TarefaForm(forms.ModelForm):
    numero_processo = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

    cliente = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput()
    )

    status = forms.ChoiceField(
        choices=Tarefa.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Status da Tarefa"
    )

    class Meta:
        model = Tarefa
        fields = '__all__'
        widgets = {
            'responsaveis': forms.Select(attrs={'class': 'form-control'}),
            'tarefa': forms.TextInput(attrs={'class': 'form-control'}),
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


