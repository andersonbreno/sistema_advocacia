from django import forms
from django.core.validators import validate_email
from .models import Parceiros

class ParceiroForm (forms.ModelForm):
    class Meta:
        model = Parceiros
        fields = [
            'parceiro', 'email_parceiro'
            ]
        widgets = {
            'parceiro': forms.TextInput(attrs={'class': 'form-control'}),
            'email_parceiro': forms.EmailInput(attrs={'class': 'form-control'}),
        }    