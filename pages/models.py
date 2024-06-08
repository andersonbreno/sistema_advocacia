from django.db import models

class DataPoint(models.Model):
    label = models.CharField(max_length=100)
    value = models.FloatField()