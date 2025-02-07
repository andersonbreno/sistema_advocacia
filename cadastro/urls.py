from django.urls import path
from . import views

app_name = "cadastro"

urlpatterns = [
    path('/list/', views.CadastroListView.as_view(), name='list'),
    path('/create/', views.CadastroCreateView.as_view(), name='create'),
    path('/<int:pk>/edit/', views.CadastroUpdateView.as_view(), name='update'),
    path('/<int:pk>/detail/', views.CadastroDetailView.as_view(), name='detail'),
    path('/<int:pk>/delete/', views.CadastroDeleteView.as_view(), name='delete'),
]