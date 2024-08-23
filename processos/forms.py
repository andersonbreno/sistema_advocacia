from django import forms
from .models import Cliente, Processo, Advogado

class ProcessoForm(forms.ModelForm):
    
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), required=True, label="Cliente")
    advogado = forms.ModelChoiceField(queryset=Advogado.objects.all(), required=True, label="Advogado")

    class Meta:
        model = Processo
        fields = '__all__'  # Garante que todos os campos sejam incluídos
        widgets = {
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'advogado': forms.TextInput(attrs={'class': 'form-control'}),
            'advogado': forms.TextInput(attrs={'class': 'form-control cpf-mask'}),
            'numero_processo': forms.NumberInput(attrs={'class': 'form-control'}),
            'grupo': forms.Select(attrs={'class': 'form-control'}),
            'fase_processo': forms.Select(attrs={'class': 'form-control'}),
            'fechou_contrato': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'data_contrato': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}), 
            'prioritario': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'arquivado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control'}),
            'pendencia': forms.Select(attrs={'class': 'form-control'}),
            # Adicione widgets personalizados para outros campos conforme necessário
        }
    def __init__(self, *args, **kwargs):
        super(ProcessoForm, self).__init__(*args, **kwargs)
        self.field['numero_processo'].required = False

    def clean(self):
        # Chama o método clean() do super para garantir que todas as validações do modelo sejam executadas
        super().clean()

        # Aqui você pode adicionar qualquer validação adicional específica do formulário, se necessário

        # Não esqueça de retornar o conjunto de dados limpos
        return self.cleaned_data
