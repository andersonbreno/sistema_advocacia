from django.contrib import admin
from .models import Cliente
from django.forms import TextInput, Textarea
from django.db import models
from django.utils.html import format_html

class ClienteAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '15'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 1, 'cols': 40})},
    }
    
    list_display = ('nome', 'cpf', 'virou_cliente', 'foto_thumbnail',)  # Inclui uma visualização em miniatura da foto se necessário
    search_fields = ['nome', 'cpf', 'email__email', 'telefone__numero']  # Atualize conforme a nova estrutura
    list_filter = ('virou_cliente',)  # Campos pelos quais pode-se filtrar na barra lateral.

    readonly_fields = ["foto_thumbnail"]  # Campo readonly para visualização da foto

    def foto_thumbnail(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="max-height: 200px;"/>', obj.foto.url)
        return "Nenhuma foto"
    foto_thumbnail.short_description = 'Pré-visualização da foto'

admin.site.register(Cliente, ClienteAdmin)
