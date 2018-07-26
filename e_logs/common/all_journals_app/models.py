from datetime import time, date, datetime, timedelta
from pyodbc import ProgrammingError, OperationalError

from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware


class Plant(models.Model):
    NUMBER_OF_SHIFTS = {
        'leaching': 2,
        'furnace': 3,
        'electrolysis': 4
    }
    name = models.CharField(null=True,
                            blank=True,
                            default='leaching',
                            max_length=128,
                            choices=(('leaching', 'Выщелачивание'),
                                     ('furnace', 'Обжиг'),
                                     ('electrolysis', 'Электролиз')))

    @property
    def number_of_shifts(self):
        return Plant.NUMBER_OF_SHIFTS[self.name]

    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'


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
    time = models.DateTimeField(verbose_name='Время', null=True, blank=True)

    @property
    def shift_start_time(self):
        shift_hour = (8 + (self.shift_order - 1) * (24 // self.plant.number_of_shifts)) % 24
        shift_time = time(hour=shift_hour)
        return make_aware(datetime.combine(self.shift_date, shift_time))

    @property
    def shift_end_time(self):
        shift_length = timedelta(hours=24 // self.plant.number_of_shifts)
        return self.shift_start_time + shift_length

    @property
    def shift_is_active(self):
        return self.shift_start_time <= timezone.now() <= self.shift_end_time

    def get_equipent(request):
        try:
            print(request)
            obj = JournalPage.objects.filter(type='equipment').exclude(equipment__isnull=True)
        except (ProgrammingError, OperationalError):
            return
        return obj.equipment.split(',')

    class Meta:
        unique_together = ['plant', 'shift_order', 'shift_date', 'journal_name']
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class CellValue(models.Model):
    journal_page = models.ForeignKey(JournalPage, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=128, verbose_name='Название таблицы')
    field_name = models.CharField(max_length=128, verbose_name='Название поля')
    index = models.IntegerField(null=True, blank=True, default=None, verbose_name='Номер строчки')
    value = models.CharField(max_length=1024, verbose_name='Значение поля')

    def __str__(self):
        return "journal_page: " + str(self.journal_page) + " table_name: " \
               + str(self.table_name) + " field_name: " + str(self.field_name) + \
               " index: " + str(self.index) + " value: " + str(self.value)

    class Meta:
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


def get_setting_value(name, plant=None, journal=None, table=None, cell=None):
    settings = Setting.objects.filter(name=name)
    if cell is not None:
        cell_settings = settings.filter(cell=cell)
        if cell_settings.count() > 0:
            return cell_settings[0].value

    if table is None and journal is None and plant is None:
        tables = Setting.objects.exclude(table__isnull=True).filter(name=name)
        if tables.count() > 0:
            table = tables[0].table
        else:
            table = None

    if table is not None:
        table_settings = settings.filter(table=table)
        if table_settings.count() > 0:
            return table_settings[0].value

    if journal is None and plant is None:
        journals = Setting.objects.exclude(journal__isnull=True).filter(name=name)
        if journals.count() > 0:
            journal = journals[0].journal
        else:
            journal = None

    if journal is not None:
        journal_settings = settings.filter(journal=journal)
        if journal_settings.count() > 0:
            return journal_settings[0].value

    if plant is None:
        plants = Setting.objects.exclude(plant__isnull=True).filter(name=name)
        if plants.count() > 0:
            plant = plants[0].plant
        else:
            plant = None

    if plant is not None:
        plant_settings = settings.filter(plant=plant)
        if plant_settings.count() > 0:
            return plant_settings[0].value

    raise ValueError("No setting for such scope")


class Setting(models.Model):
    name = models.CharField(max_length=128, verbose_name='Название')
    value = models.CharField(max_length=128, verbose_name='Значение')
    plant = models.CharField(max_length=128, verbose_name='Цех', blank=True, null=True)
    journal = models.CharField(max_length=128, verbose_name='Журнал', blank=True, null=True)
    table = models.CharField(max_length=128, verbose_name='Таблица', blank=True, null=True)
    cell = models.CharField(max_length=128, verbose_name='Ячейка', blank=True, null=True)
