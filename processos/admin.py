from django.contrib import admin

from processos.models import Processo, Advogado

@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'numero_processo', 'get_fase_processo_display', 'get_grupo_display')
    list_select_related = ('cliente',)  # Otimiza consultas ao banco de dados
    list_filter = ('numero_processo',) 

    def get_fase_processo_display(self, obj):
        return obj.get_fase_processo_display()
    get_fase_processo_display.admin_order_field = 'fase_processo'
    get_fase_processo_display.short_description = 'Fase do processo'

    def get_grupo_display(self, obj):
        return obj.get_grupo_display()
    get_grupo_display.admin_order_field = 'grupo'
    get_grupo_display.short_description = 'Grupo'

@admin.register(Advogado)
class AdvogadoAdmin(admin.ModelAdmin):
    list_display = ('nome'),

    # def tipo_processo(self, obj):
    #     # Se 'Tipo de processo' é um campo no seu modelo, você pode simplesmente retorná-lo.
    #     # Substitua 'tipo_processo' pelo campo real no seu modelo.
    #     return obj.tipo_processo


    # ... outras configurações do ModelAdmin ...


