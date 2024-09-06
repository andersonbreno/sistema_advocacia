from django.urls import path
from . import views

app_name = 'parceiros'

urlpatterns = [
    path('lista/', views.ParceirosListView.as_view(), name='list'),
    path('novo/', views.ParceirosCreateView.as_view(), name='create'),    
    path('<int:pk>/detalhe/', views.ParceirosDetailView.as_view(), name='detail'),
    path('<int:pk>/editar/', views.ParceirosUpdateView.as_view(), name='update'),    
    path('<int:pk>/excluir/', views.ParceirosDeleteView.as_view(), name='delete'),
    
]
