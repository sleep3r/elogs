from django.db import models
from django.utils import timezone


class Equipment(models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name='Наименование узла и характеристика дефектов')
