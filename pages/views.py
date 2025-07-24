from django.shortcuts import redirect, render
from django.views.generic import View
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from django.http import JsonResponse
from django.views import View
from django.db.models import Q
from clientes.models import Cliente
from processos.models import Processo


#from plotly.graph_objs import Bar

from django.db.models.functions import TruncMonth
from django.db.models import Count
#from plotly.offline import plot
#import plotly.graph_objs as go
import json
from .models import DataPoint
from .forms import DataPointFormSet
#import plotly.express as px
#import pandas as pd

import logging

logger = logging.getLogger(__name__)

def custom_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

# Importe os modelos que você precisa para o dashboard
# @method_decorator(never_cache, name='dispatch')

class DashboardView(View):
    template_name = 'pages/index.html'

    def get(self, request, *args, **kwargs):
        # Aqui você pode adicionar a lógica para buscar os dados que você precisa

        # Número total de clientes
        total_clientes = Cliente.objects.count()

        # Número total de processos
        total_processos = Processo.objects.count()

        # Agrupa os processos por mês e conta quantos existem por mês
        # Supondo que você adicionou o campo 'data_criacao' como discutido anteriormente
        # processos_por_mes = Processo.objects.annotate(mes=TruncMonth('data_criacao')).values('mes').annotate(total=Count('id')).order_by('mes')
        
        # Convertendo para o formato esperado pelo JavaScript
        # labels = [processo['mes'].strftime('%b') for processo in processos_por_mes]
        # data = [processo['total'] for processo in processos_por_mes]

        context = {
            'total_clientes': total_clientes,
            'total_processos': total_processos,
            # 'processos_por_mes_labels': labels,
            # 'processos_por_mes_data': data,
            # Adicione mais contextos conforme necessário
        }

        return render(request, self.template_name, context)
    
# class GraficosView(View):
#     template_name = 'pages/graficos.html'
#     form_class = GraficoForm

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             titulo = form.cleaned_data['titulo']
#             eixo_x = form.cleaned_data['eixo_x'].split(',')
#             eixo_y = [int(y) for y in form.cleaned_data['eixo_y'].split(',')]
#             grafico_html = plot([Bar(x=eixo_x, y=eixo_y)], output_type='div')

#             # Salvar o gráfico no banco de dados
#             grafico = Grafico(titulo=titulo, grafico_html=grafico_html)
#             grafico.save()

#             return render(request, self.template_name, {'form': form, 'grafico': grafico_html})

class DataPointCreateView(FormView):
    # model = DataPoint
    template_name = 'pages/create_chart.html'
    form_class = DataPointFormSet
    success_url = reverse_lazy('pages:view_chart')

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=DataPoint.objects.none())
        return self.render_to_response(self.get_context_data(form=formset))

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        logger.debug(f"POST data: {request.POST}")
        if formset.is_valid():
            data = [form.cleaned_data for form in formset.forms if form.cleaned_data]
            logger.debug(f"Data collected from form: {data}")
            request.session['chart_data'] = data
            return self.form_valid(formset)
        else:
            logger.error(f"Formset is not valid: {formset.errors}")
            return self.form_invalid(formset)

    def form_valid(self, form):
        return super().form_valid(form)
        

class ChartView(TemplateView):
    template_name = 'pages/view_chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.request.session.get('chart_data', [])
        logger.debug(f"Data retrieved from session: {data}")
        if data and len(data) > 0:
            df = pd.DataFrame(data)
            df = df.dropna()  # Remove rows with missing data
            logger.debug(f"DataFrame after dropping NAs: {df}")
            if not df.empty:  # Check again after dropping rows with missing data
                df['color'] = df['label']
                fig = px.bar(df, x='label', y='value', color='color', color_discrete_sequence=px.colors.qualitative.Alphabet)
                context['chart'] = fig.to_html(full_html=False)
            else:
                context['chart'] = 'Nenhum dado disponível para exibir o gráfico.'
        else:
            context['chart'] = 'Nenhum dado disponível para exibir o gráfico.'
        return context
        

class BuscaGlobalView(View):
    def get(self, request):
        query = request.GET.get('term', '').strip()
        if not query:
            return JsonResponse({'message': 'No query provided'}, status=400)

        try:
            clientes = Cliente.objects.filter(nome__icontains=query)[:5]
            processos = Processo.objects.filter(numero_processo__icontains=query)[:5]

            resultados = [
                {'id': cliente.id, 'nome': cliente.nome, 'tipo': 'cliente', 'icon': 'fa-user', 'detail_url': f'/clientes/{cliente.id}/'} 
                for cliente in clientes
            ] + [
                {'id': processo.id, 'nome': processo.numero_processo, 'tipo': 'processo', 'icon': 'fa-gavel', 'detail_url': f'/processos/{processo.id}/'} 
                for processo in processos
            ]

            return JsonResponse(resultados, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
# class BuscaGlobalView(View):
#     def get(self, request):
#         query = request.GET.get('term', '')
#         clientes = Cliente.objects.filter(nome__icontains=query)[:5]
#         processos = Processo.objects.filter(numero_processo__icontains=query)[:5]

#         resultados = []

#         # Adicionando clientes ao resultado
#         for cliente in clientes:
#             resultados.append({
#                 'id': cliente.id,
#                 'nome': cliente.nome,
#                 'tipo': 'cliente',  # Adiciona o tipo manualmente
#             })

#         # Adicionando processos ao resultado
#         for processo in processos:
#             resultados.append({
#                 'id': processo.id,
#                 'nome': processo.numero_processo,  # Mostra o número do processo
#                 'tipo': 'processo',  # Adiciona o tipo manualmente
#             })

#         return JsonResponse(resultados, safe=False)


# Adicione a URL correspondente em urls.py
# path('', DashboardView.as_view(), name='index'),



# from django.contrib.auth.mixins import LoginRequiredMixin
# class DashboardView(LoginRequiredMixin, View):
#     template_name = 'pages/index.html'  # Seu template do dashboard

#     def get(self, request, *args, **kwargs):
#         # Aqui você pode adicionar a lógica para buscar os dados que você precisa
#         # Por exemplo, o número de clientes, processos, etc.
#         context = {
#             #'clientes_count': Cliente.objects.count(),
#             #'processos_count': Processo.objects.count(),
#             # Adicione mais contextos conforme necessário
#         }
#         return render(request, self.template_name, context)