from django.urls import path
from . import views

app_name = 'tarefas'

urlpatterns = [
    path('', views.TarefaListView.as_view(), name='list'),
    path('<int:pk>/', views.TarefaDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.TarefaUpdateView.as_view(), name='tarefa-update'),
    path('<int:pk>/excluir/', views.TarefaDeleteView.as_view(), name='delete'),
    path('<int:pk>/duplicar/', views.tarefa_duplicar_view, name='tarefa-duplicar'),
]
