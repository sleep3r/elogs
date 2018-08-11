from datetime import time, datetime, timedelta

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.timezone import make_aware

from e_logs.core.utils.webutils import get_or_none


class Plant(models.Model):
    name = models.CharField(default='leaching',
                            verbose_name='Название цеха',
                            max_length=128,
                            choices=(('leaching', 'Выщелачивание'),
                                     ('furnace', 'Обжиг'),
                                     ('electrolysis', 'Электролиз')))
    settings = GenericRelation('core.Setting', related_query_name='plant')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='plant')

    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'


class Journal(models.Model):
    """Abstract journal entity."""

    name = models.CharField(max_length=128, verbose_name='Название журнала')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='journals')
    type = models.CharField(max_length=128,
                            choices=(
                                ('shift', 'Смена'),
                                ('equipment', 'Оборудование'),
                                ('measurement', 'Измерение'),
                                ('month', 'Месяц'),
                                ('year', 'Год')
                            ),
                            default='shift',
                            verbose_name='Тип'
                            )
    settings = GenericRelation('core.Setting', related_query_name='journal')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='journal')

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class Table(models.Model):
    """Abstract table entity."""

    name = models.CharField(max_length=128, verbose_name='Название таблицы')
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='tables')
    settings = GenericRelation('core.Setting', related_query_name='table')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='table')

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'


class Field(models.Model):
    """Abstract field entity."""

    name = models.CharField(max_length=128, verbose_name='Название поля')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='fields')
    settings = GenericRelation('core.Setting', related_query_name='field')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='field')

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'


class CellGroup(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)


class Measurement(CellGroup):
    time = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала смены')


class Shift(CellGroup):
    order = models.IntegerField(verbose_name='Номер смены')
    date = models.DateField(verbose_name='Дата начала смены')

    @cached_property
    def start_time(self):
        number_of_shifts = Shift.get_number_of_shifts(self.journal)
        shift_hour = (8 + (self.order - 1) * (24 // number_of_shifts)) % 24
        shift_time = time(hour=shift_hour)
        return make_aware(datetime.combine(self.date, shift_time))

    @property
    def end_time(self):
        number_of_shifts = Shift.get_number_of_shifts(self.journal)
        shift_length = timedelta(hours=24 // number_of_shifts)
        return self.start_time + shift_length

    @property
    def is_active(self):
        return self.start_time <= timezone.now() <= self.end_time

    @staticmethod
    def get_number_of_shifts(object):
        # avoiding import loop
        from e_logs.core.models import Setting
        return int(Setting.get_value(name='number_of_shifts', obj=object))

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class Equipment(CellGroup):
    name = models.CharField(
        max_length=1024,
        verbose_name='Название оборудования',
        default=''
    )


class Cell(models.Model):
    """Specific cell in some table."""

    group = models.ForeignKey(CellGroup, on_delete=models.CASCADE, related_name='data')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='cells')
    index = models.IntegerField(default=None, verbose_name='Номер строчки')
    value = models.CharField(max_length=1024, verbose_name='Значение поля', blank=True, default='')
    responsible = models.ForeignKey('login_app.Employee', on_delete=models.SET_NULL, null=True)
    comments = GenericRelation('all_journals_app.Comment', related_query_name='cell')

    @property
    def name(self):
        return self.field.name

    @name.setter
    def name(self, value):
        self.field.name = value
        self.field.save()

    @staticmethod
    def get(cell):
        return get_or_none(Cell, **cell)

    class Meta:
        unique_together = ['field', 'index', 'group']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'


class Comment(models.Model):
    text = models.CharField(max_length=2048, verbose_name='Текст комментария', default='')
    employee = models.ForeignKey('login_app.Employee', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('content_type', 'object_id')
