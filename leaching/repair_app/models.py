import datetime

from django.db import models


# Аггрегатный журнал технологического оборудования
# class AggregatedTechnicalJournal(models.Model):
#     create_time = models.DateTimeField(verbose_name='Время анализа/создания записи', default=datetime.datetime.now)
#
#     date = models.DateTimeField(verbose_name='Дата обнаружения неисправности')
#     name = models.CharField(max_length=1024, blank=True, verbose_name='ФИО ответственного лица')
#     comment = models.CharField(max_length=1024, blank=True, verbose_name='Сведения о замене и ремонте')


class Repairs(models.Model):
    create_time = models.DateTimeField(verbose_name='Время анализа/создания записи', default=datetime.datetime.now)

    date = models.DateTimeField(verbose_name='Дата осмотра')
    name = models.CharField(max_length=1024, blank=True, verbose_name='Наименование узла и характеристика дефектов')
    comment = models.CharField(max_length=1024, blank=True, verbose_name='Дата и объем выполненных работ по устранению'
                                                                         ' неисправностей')