from django.urls import path
from . import views

app_name = 'parceiros'

urlpatterns = [
    path('parceiros_lista/', views.ParceirosListView.as_view(), name='list'),
    path('parceiros_novo/', views.ParceirosCreateView.as_view(), name='parceiro-create'),    
    path('<int:pk>/parceiros_detalhe/', views.ParceirosDetailView.as_view(), name='parceiro-detail'),
    path('<int:pk>/parceiros_editar/', views.ParceirosUpdateView.as_view(), name='parceiro-update'),    
    path('<int:pk>/parceiros_excluir/', views.ParceirosDeleteView.as_view(), name='parceiro-delete'),
    
]
