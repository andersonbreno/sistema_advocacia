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
            'parceiro': forms.TextInput(atrrs={'class': 'form-control'}),
            'email_parceiro': forms.TextInput(atrrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(ParceiroForm, self).__init__(*args, **kwargs)

        self.fields['parceiro'].required = False