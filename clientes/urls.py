from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('lista/', views.ClienteListView.as_view(), name='list'),
    path('novo/', views.ClienteCreateView.as_view(), name='create'),
    path('<int:pk>/detalhe/', views.ClienteDetailView.as_view(), name='cliente-detail'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='cliente-update'),
    path('<int:pk>/excluir/', views.ClienteDeleteView.as_view(), name='cliente-delete'),
]
