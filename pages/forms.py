from django import forms
from django.shortcuts import render
from django.views import View
#from plotly.offline import plot
#from plotly.graph_objs import Bar

from .models import DataPoint

from django.forms import modelformset_factory

DataPointFormSet = modelformset_factory(DataPoint, fields=('label', 'value'), extra=3)