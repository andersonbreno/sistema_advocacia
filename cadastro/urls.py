from django.urls import path
from .views import (
    CadastroCreateView,
    CadastroDeleteView,
    CadastroDetailView,
    CadastroUpdateView,
    CadastroListView,
)

app_name = "cadastro"

urlpatterns = [
    path('create/', CadastroCreateView.as_view(), name='create'),
    path('<int:pk>/delete/', CadastroDeleteView.as_view(), name='delete'),
    path('<int:pk>/detail/', CadastroDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', CadastroUpdateView.as_view(), name='update'),   
    path('list/', CadastroListView.as_view(), name='list'),
]