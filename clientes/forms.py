from django import forms
from django.core.validators import validate_email

from .widgets import DatePickerInput
from .models import Cliente
# from .validators import validar_cpf
from .widgets import ImageInput

class ClienteForm(forms.ModelForm):
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
                
      
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        # Verifica se é uma edição (instance existe e tem PK)
        if self.instance and self.instance.pk:
            # Se o CPF não foi alterado, não precisa validar
            if self.instance.cpf == cpf:
                return cpf
        # Validação para novo cadastro ou CPF alterado
        if Cliente.objects.filter(cpf=cpf).exists():
            raise forms.ValidationError("Cliente com este CPF já existe.")
        return cpf
    
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
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = ''.join(filter(str.isdigit, telefone))
            if len(telefone) != 11:
                raise forms.ValidationError('O telefone deve conter exatamente 11 dígitos.')
        return telefone
    
    def clean_field(self):
        data = self.cleaned_data["field"]
        
        return data
    
    #def clean(self):
        #cleaned_data = super().clean()
        #foto = cleaned_data.get('foto')
        #if not foto and not self.instance.foto:
            #self.add_error('foto', 'Por favor, capture uma foto para continuar.')
        #return cleaned_data
