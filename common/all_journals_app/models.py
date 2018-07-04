from django.db import models
from datetime import time, date, datetime, timedelta


class Plant(models.Model):
    name = models.CharField(null=True,
                             blank=True,
                             default='leaching',
                             max_length=128,
                             choices=(('leaching', 'Выщелачивание'),
                                      ('furnace', 'Обжиг'),
                                      ('electrolysis', 'Электролиз')))
    number_of_shifts = models.IntegerField(null=True,
                                      blank=True,
                                      default=1,
                                      verbose_name='Количестов смен')


class JournalPage(models.Model):
    type = models.CharField(max_length=128, choices=(('shift', 'Смена'),
                                                     ('equipment', 'Оборудование'),
                                                     ('month', 'Месяц')))
    journal_name = models.CharField(max_length=256, verbose_name='Название журнала')

    # for shift type
    plant = models.ForeignKey('Plant', on_delete=models.SET_NULL, null=True)
    shift_order = models.IntegerField(null=True,
                                      blank=True,
                                      default=1,
                                      verbose_name='Номер смены')
    shift_date = models.DateField(null=True,
                                  blank=True,
                                  default=date(year=1999, month=6, day=15),
                                  verbose_name='Дата начала смены')

    @property
    def shift_start_time(self):
        shift_hour = (8 + (self.shift_order-1) * self.plant.number_of_shifts) % 24
        shift_time = time(hour=shift_hour)
        return datetime.combine(self.shift_date, shift_time)

    @property
    def shift_end_time(self):
        shift_length = timedelta(hours=24 // self.plant.number_of_shifts)
        return self.shift_start_time + shift_length

    class Meta:
        unique_together = ['plant', 'shift_order', 'shift_date', 'journal_name']


class CellValue(models.Model):
    journal_page = models.ForeignKey(JournalPage, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=128, verbose_name='Название таблицы')
    field_name = models.CharField(max_length=128, verbose_name='Название поля')
    index = models.IntegerField(null=True, blank=True, default=None, verbose_name='Номер строчки')
    value = models.CharField(max_length=1024, verbose_name='Значение поля')
    responsible = models.ForeignKey('login_app.Employee', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "journal_page: " + str(self.journal_page) + " table_name: " \
               + str(self.table_name) + " field_name: " + str(self.field_name) +\
               " index: " + str(self.index) + " value: " + str(self.value)
