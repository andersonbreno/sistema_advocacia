from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Parceiros(models.Model):
    parceiro = models.CharField(max_length=150)
    email_parceiro = models.EmailField(blank=True)          
        
    def __str__(self):
        return self.nome
