from django.urls import path
from .views import CadastroView

app_name = 'cadastro'

urlpatterns = [
    path('cadastro/', CadastroView.as_view(), name='cadastro'),
    path('cadastro/<int:cliente_id>/<int:processo_id>/<int:parceiro_id>/', CadastroView.as_view(), name='cadastro_view_edit'),
]
