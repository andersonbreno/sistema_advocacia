from django.urls import path
from . import views
from .views import DataPointCreateView, ChartView


app_name = 'pages'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('busca-global/', views.BuscaGlobalView.as_view(), name='busca_global'),
    # path('graficos/', views.GraficosView.as_view(), name='graficos'),
    path('create_/', views.DataPointCreateView.as_view(), name='create_'),
    path('view_chart/', views.ChartView.as_view(), name='view_chart'),
]
