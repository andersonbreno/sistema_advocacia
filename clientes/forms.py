from django import forms
from django.core.validators import validate_email
from .models import Cliente
# from .validators import validar_cpf
from .widgets import ImageInput

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = [
            'nome','cpf','data_de_nascimento', 'estado_civil', 'profissao',
            'virou_cliente', 'cadastrado_advbox', 'cadastrado_planilha',
            'justificativa', 'descricao', 'foto', 'email', 'telefone',
            'whatsapp', 'cep', 'rua', 'numero', 'complemento', 'bairro',
            'cidade', 'estado'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control cpf-mask'}),
            'data_de_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control'}),
            'profissao': forms.TextInput(attrs={'class': 'form-control'}),
            'virou_cliente': forms.Select(attrs={'class': 'form-control'}),
            'cadastrado_advbox': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-input'}),
            'cadastrado_planilha': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-input'}),
            'justificativa': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'foto': ImageInput(attrs={'class': 'form-control'}),
            # Campos adicionados diretamente no modelo Cliente
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control mask-telefone', 'maxlength': '15'}),
            'whatsapp': forms.CheckboxInput(attrs={'class': 'form-check-input checkbox-input'}),
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
        self.fields['data_de_nascimento'].input_formats = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y']

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if Cliente.objects.filter(cpf=cpf).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cliente com este CPF já existe.")
        return cpf
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Cliente.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este email já está em uso.")
        return email
    
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone:
            telefone = ''.join(filter(str.isdigit, telefone))
            if len(telefone) != 11:
                raise forms.ValidationError('O telefone deve conter exatamente 11 dígitos.')
        return telefone


    #def clean(self):
        #cleaned_data = super().clean()
        #foto = cleaned_data.get('foto')
        #if not foto and not self.instance.foto:
            #self.add_error('foto', 'Por favor, capture uma foto para continuar.')
        #return cleaned_data
