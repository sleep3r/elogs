from django.db import models
from datetime import time, date, datetime, timedelta


class JournalPage(models.Model):
    type = models.CharField(max_length=128, choices=(('shift', 'Смена'),
                                                     ('equipment', 'Оборудование'),
                                                     ('month', 'Месяц'),
                                                     ('year', 'Год')), verbose_name='Тип')
    journal_name = models.CharField(max_length=256, verbose_name='Название журнала')

    # for shift type
    plant = models.ForeignKey('Plant', on_delete=models.SET_NULL, null=True, verbose_name='Цех')
    shift_order = models.IntegerField(blank=True, null=True, verbose_name='Номер смены')
    shift_date = models.DateField(blank=True, null=True, verbose_name='Дата начала смены')
    date = models.DateField(blank=True, null=True, verbose_name='Дата')
    year = models.IntegerField(blank=True, null=True, verbose_name='Год')
    month = models.IntegerField(blank=True, null=True, verbose_name='Месяц')
    equipment = models.CharField(max_length=256, null=True, verbose_name='Оборудование')

    @property
    def shift_start_time(self):
        shift_hour = (8 + (self.shift_order-1) * (24//self.plant.number_of_shifts)) % 24
        shift_time = time(hour=shift_hour)
        return datetime.combine(self.shift_date, shift_time)

    @property
    def shift_end_time(self):
        shift_length = timedelta(hours=24 // self.plant.number_of_shifts)
        return self.shift_start_time + shift_length

    @property
    def shift_is_active(self):
        return self.shift_start_time <= datetime.now() <= self.shift_end_time

    class Meta:
        unique_together = ['plant', 'shift_order', 'shift_date', 'journal_name']
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'

class Cell(models.Model):
    journal_page = models.ForeignKey(JournalPage, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=128, verbose_name='Название таблицы')
    field_name = models.CharField(max_length=128, verbose_name='Название поля')
    index = models.IntegerField(null=True, blank=True, default=None, verbose_name='Номер строчки')

class Setting(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    value = models.CharField(max_length=128, verbose_name='Значение')
    scope = models.CharField(max_length=128, verbose_name='Область')
