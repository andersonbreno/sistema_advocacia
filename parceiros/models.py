from django.db import models

class Parceiro(models.Model):
    parceiro = models.CharField(max_length=150)
    email_parceiro = models.EmailField(blank=True)          
        
    def __str__(self):
        return self.parceiro
