import datetime

from django.db import models


# Create your models here.
class CuPulpAnal(models.Model):
    create_time = models.DateTimeField(verbose_name='Время анализа/создания записи', default=datetime.datetime.now)

    date = models.DateTimeField(verbose_name='Дата обнаружения неисправности')
    name = models.CharField(max_length=1024, blank=True, verbose_name='ФИО ответственного лица')
    comment = models.CharField(max_length=1024, blank=True, verbose_name='Сведения о замене и ремонте')