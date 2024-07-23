from django.urls import path
from . import views

app_name = 'parceiros'

urlpatterns = [
    path('parceiros_lista/', views.ParceirosListView.as_view(), name='list'),
    path('parceiros_novo/', views.ParceirosCreateView.as_view(), name='parceiros_create'),
    path('centrodecusto_novo/', views.CentrodeCustoCreateView.as_view(), name='centrodecusto_create'),
    path('<int:pk>/parceiros_detalhe/', views.ParceirosDetailView.as_view(), name='parceiros-detail'),
    path('<int:pk>/parceiros_editar/', views.ParceirosUpdateView.as_view(), name='parceiros-update'),
    path('<int:pk>/centrodecusto_editar/', views.CentrodeCustoUpdateView.as_view(), name='centrodecusto-update'),
    path('<int:pk>/parceiros_excluir/', views.ParceirosDeleteView.as_view(), name='parceiros-delete'),
    path('<int:pk>/centrodecusto_excluir/', views.CentrodeCustoDeleteView.as_view(), name='centrodecusto-delete'),
]
