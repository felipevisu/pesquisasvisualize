import os

from django.db import models
from django.dispatch import receiver

from apps.surveys.models import OpenSurvey, RegionalSurvey

class Client(models.Model):
    name = models.CharField('nome da empresa', max_length=100)
    creation_date = models.DateTimeField('data de criação', auto_now_add=True)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural= 'Clientes'

    def __str__(self):
        return self.name