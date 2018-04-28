from django.db import models


# Аггрегатный журнал технологического оборудования
# class AggregatedTechnicalJournal(models.Model):
#     create_time = models.DateTimeField(verbose_name='Время анализа/создания записи', default=datetime.datetime.now)
#
#     date = models.DateTimeField(verbose_name='Дата обнаружения неисправности')
#     name = models.CharField(max_length=1024, blank=True, verbose_name='ФИО ответственного лица')
#     comment = models.CharField(max_length=1024, blank=True, verbose_name='Сведения о замене и ремонте')
from django.utils import timezone


class Equipment(models.Model):
    name = models.CharField(max_length=256, blank=True, verbose_name='Наименование узла и характеристика дефектов')


class Repairs(models.Model):
    create_time = models.DateTimeField(verbose_name='Время анализа/создания записи', default=timezone.now)

    date = models.DateTimeField(verbose_name='Дата осмотра')
    name = models.CharField(max_length=1024, blank=True, verbose_name='Наименование узла и характеристика дефектов')
    date_performed = models.DateTimeField(verbose_name='Дата выполненных работ', default=timezone.now)
    comment = models.CharField(max_length=1024, blank=True, verbose_name='Объем выполненных работ по устранению'
                                                                         ' неисправностей')
    equipment = models.ForeignKey(Equipment, on_delete=models.SET_NULL, null=True,
                                  verbose_name='Оборудование', related_name='repairs')