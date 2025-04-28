"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import RedirectView
from config import settings

admin.site.site_header = settings.ADMIN_SITE_HEADER
admin.site.site_title = settings.ADMIN_SITE_TITLE
admin.site.index_title = settings.ADMIN_INDEX_TITLE


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(('pages.urls', 'pages'), namespace='pages')),  # Inclui as URLs do app pages
    path('cadastro/', include('cadastro.urls')), # Inclui as URLs do app cadastro
    # path('clientes/', include('clientes.urls')),  # Inclui as URLs do app clientes
    path('parceiros/', include('parceiros.urls')), # Inclui as URLs do app parceiros
    # path('processos/', include('processos.urls')),  # Inclui as URLs do app processos
    # path('tarefas/', include('tarefas.urls')), # Inclui as URLs do app tarefas
    path('', include('usuarios.urls')),
    # Redirecionar /favicon.ico para o favicon nos arquivos estáticos
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)