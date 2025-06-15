from django import forms
from datetime import datetime
from .widgets import DatePickerInput
from .models import Cliente
from .validators import validar_cpf, validar_cep, validar_telefone
from .widgets import ImageInput
import re

class ClienteForm(forms.ModelForm):
    data_de_nascimento = forms.DateField(
        widget=DatePickerInput(attrs={'class': 'form-control'}),
        input_formats=['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%d-%m-%Y'],
        required=False
    )
    
    class Meta:
        model = Cliente
        fields = [
            'nome','cpf','data_de_nascimento', 'estado_civil', 'profissao',
            'virou_cliente', 'origem_cadastrado','justificativa', 'descricao', 'foto', 'email', 'telefone',
            'whatsapp', 'cep', 'rua', 'numero', 'complemento', 'bairro',
            'cidade', 'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control cpf-mask'}),
            'data_de_nascimento': DatePickerInput(attrs={'class': 'form-control'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'profissao': forms.TextInput(attrs={'class': 'form-control'}),
            'virou_cliente': forms.Select(attrs={'class': 'form-control'}),
            'origem_cadastrado': forms.Select(attrs={'class': 'form-control'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': ImageInput(attrs={'class': 'form-control'}),
            # Campos adicionados diretamente no modelo Cliente
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mask-telefone', 'maxlength': '15'}),
            'whatsapp': forms.Select(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control mask-cep'}),
            'rua': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'complemento': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(ClienteForm, self).__init__(*args, **kwargs)
        
        self.fields['profissao'].required = False
        self.fields['foto'].required = False
        self.fields['telefone'].required = True
       
    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Verifica se é uma edição (instance existe e tem PK)
        if self.instance and self.instance.pk:
            # Se o email não foi alterado, não precisa validar
            if self.instance.email == email:
                return email
        # Validação para novo cadastro ou email alterado
        if email and Cliente.objects.filter(email=email).exists():  # Verifica se email não é vazio
            raise forms.ValidationError("Este email já está em uso.")
        return email
        
    def clean_data_de_nascimento(self):
        data_nascimento = self.cleaned_data.get('data_de_nascimento')
        if isinstance(data_nascimento, str):
            try:
                return datetime.strptime(data_nascimento, '%Y-%m-%d').date()
            except ValueError:
                raise forms.ValidationError("Formato de data inválido. Use DD/MM/AAAA ou AAAA-MM-DD")
        
        return data_nascimento
    
    def clean(self):
        cleaned_data = super().clean()
        
        # Formata os campos antes de salvar
        if 'cpf' in cleaned_data:
            cleaned_data['cpf'] = re.sub(r'[^\d]', '', cleaned_data['cpf'])
        
        if 'cep' in cleaned_data:
            cleaned_data['cep'] = re.sub(r'[^\d]', '', cleaned_data['cep'])
        
        if 'telefone' in cleaned_data:
            cleaned_data['telefone'] = re.sub(r'[^\d]', '', cleaned_data['telefone'])
        
        return cleaned_data
    
    def clean_field(self):
        data = self.cleaned_data["field"]
        
        return data
    
    #def clean(self):
        #cleaned_data = super().clean()
        #foto = cleaned_data.get('foto')
        #if not foto and not self.instance.foto:
            #self.add_error('foto', 'Por favor, capture uma foto para continuar.')
        #return cleaned_data
