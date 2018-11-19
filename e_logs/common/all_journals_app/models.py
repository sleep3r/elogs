import json
from datetime import time, datetime, timedelta, date

from cacheops import cached_as, cached
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.timezone import make_aware
from django_extensions.db.models import TimeStampedModel

from e_logs.core.utils.webutils import none_if_error, logged, default_if_error, \
    max_cache, current_date


class Plant(models.Model):
    name = models.CharField(default='leaching',
                            verbose_name='Цех',
                            max_length=128,
                            choices=(('leaching', 'Выщелачивание'),
                                     ('furnace', 'Обжиг'),
                                     ('electrolysis', 'Электролиз')))
    settings = GenericRelation('core.Setting', related_query_name='plant', related_name='plants')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='plant',
                                related_name='plants')

    verbose_name = models.CharField(max_length=128, verbose_name='Название цеха')

    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'


class Journal(models.Model):
    """Abstract journal entity."""

    name = models.CharField(max_length=128, verbose_name='Журнал')
    verbose_name = models.CharField(max_length=256, verbose_name='Название журнала')
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
    settings = GenericRelation('core.Setting', related_query_name='journal',
                               related_name='journals')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='journal',
                               related_name='journals')

    @property
    def group(self):
        return ContentType.objects.get(model=self.type).model_class()


    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class Table(models.Model):
    """Abstract table entity."""

    name = models.CharField(max_length=128, verbose_name='Таблица')
    verbose_name = models.CharField(max_length=256, verbose_name='Название таблицы')
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='tables')
    settings = GenericRelation('core.Setting', related_query_name='table', related_name='setting_tables')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='table',
                               related_name='comment_tables')

    @cached_property
    def plant(self):
        return self.journal.plant

    def cells(self, page):
        def cached_cells(self, page):
            qs = Cell.objects.select_related('field', 'field__table').cache() \
                .filter(group=page, field__table=self)
            return qs
        return cached_cells(self, page)

    def get_fields(self):
        return self.fields.all()

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'


class Field(models.Model):
    """Abstract field entity."""

    name = models.CharField(max_length=128, verbose_name='Столбец')
    formula = models.CharField(max_length=4000, verbose_name='Формула', null=True, default="")
    verbose_name = models.CharField(max_length=256, verbose_name='Название столбца')
    type = models.CharField(max_length=128, default="", null=True)
    units = models.CharField(max_length=128, default="", null=True)
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='fields')
    settings = GenericRelation('core.Setting', related_query_name='setting_field',
                               related_name='setting_fields')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='comment_field',
                               related_name='comment_fields')

    # @cached_property
    # def type(self):
    #     return self.settings.get(name='field_description').val()['type']
    #
    # @cached_property
    # @default_if_error('')
    # def units(self):
    #     return self.settings.get(name='field_description').val()['units']

    @cached_property
    @default_if_error([])
    def options(self):
        return self.settings.get(name='field_description').val()['options']

    @cached_property
    def plant(self):
        @cached(Plant, Journal, Table, Field)
        def cached_plant(self):
            return self.table.journal.plant
        return cached_plant()

    @cached_property
    def journal(self):
        return self.table.journal

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

        indexes = [
            models.Index(fields=['name']),
        ]


class CellGroup(models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def tables(self):
        @cached(timeout=60*60*3)
        def cached_tables(self):
            return list(self.journal.tables.all())

        return cached_tables(self)


class Shift(CellGroup):
    order = models.IntegerField(verbose_name='Порядок смены')
    date = models.DateField(verbose_name='Дата начала смены')
    closed = models.BooleanField(default=False)
    ended = models.BooleanField(default=False)
    responsibles = models.ManyToManyField('login_app.Employee')

    class Meta:
        verbose_name = 'Смена'
        verbose_name_plural = 'Смены'

    @property
    def start_time(self) -> timezone.datetime:
        number_of_shifts = Shift.get_number_of_shifts(self.journal)
        shift_hour = (8 + (self.order - 1) * (24 // int(number_of_shifts))) % 24
        shift_time = time(hour=shift_hour, tzinfo=timezone.get_current_timezone())
        return datetime.combine(self.date, shift_time)

    @property
    def end_time(self) -> timezone.datetime:
        number_of_shifts = Shift.get_number_of_shifts(self.journal)
        shift_length = timedelta(hours=24 // int(number_of_shifts))
        return self.start_time + shift_length

    def is_active(self, time=timezone.now()) -> bool:
        return self.start_time <= timezone.localtime(time) <= self.end_time

    @staticmethod
    def get_number_of_shifts(obj) -> int:
        from e_logs.core.models import Setting # avoiding import loo

        @cached_as(Setting.objects.filter(name='number_of_shifts'))
        def cached_number_of_shifts(obj):
            return Setting.of(obj)['number_of_shifts']

        return cached_number_of_shifts(obj)

    @staticmethod
    def get_or_create(journal: Journal, shift_order: int, shift_date: timezone.datetime) -> 'Shift':
        return Shift.objects.prefetch_related('journal', 'journal__plant', 'journal__plant').cache()\
            .get_or_create(journal=journal, order=shift_order, date=shift_date)[0]

    @staticmethod
    @logged
    def get_shift(journal, pid=None) -> 'Shift':
        shift = None

        if pid:
            shift = Shift.objects.get(id=pid)
        else:
            number_of_shifts = Shift.get_number_of_shifts(journal)
            assert number_of_shifts > 0, "<= 0 number of shifts"

            # create shifts for today and return current shift
            for shift_order in range(1, number_of_shifts + 1):
                shift = Shift.objects.get_or_create(journal=journal,
                                                    order=shift_order,
                                                    date=current_date())[0]
                if shift.is_active():
                    break

        return shift


class Equipment(CellGroup):
    name = models.CharField(max_length=1024, verbose_name='Название оборудования', default='')


class Year(CellGroup):
    year_date = models.IntegerField(verbose_name='Год')


class Month(CellGroup):
    month_date = models.CharField(max_length=16, verbose_name='Месяц')
    month_order = models.IntegerField(verbose_name='Номер месяца')
    year_date = models.IntegerField(verbose_name='Год')


class Cell(TimeStampedModel):
    """Specific cell in some table."""

    group = models.ForeignKey(CellGroup, on_delete=models.CASCADE, related_name='group_cells')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='cells')
    index = models.IntegerField(default=None, verbose_name='Номер строчки')
    value = models.CharField(max_length=1024, verbose_name='Значение поля', blank=True, default='')
    responsible = models.ForeignKey('login_app.Employee', on_delete=models.SET_NULL, null=True)
    comments = GenericRelation('all_journals_app.Comment', related_query_name='cell')

    @cached_property
    @max_cache
    def journal(self) -> Journal:
        return self.field.table.journal

    @cached_property
    @max_cache
    def table(self) -> Table:
        return self.field.table

    @cached_property
    @max_cache
    def name(self) -> str:
        return self.field.name

    @staticmethod
    @none_if_error
    def get_by_addr(field_name, table_name, group_id, index):
        manager = Cell.objects.select_related('field', 'field__table').cache()
        res = manager.get(field__name=field_name, field__table__name=table_name,
                          group_id=group_id, index=index)
        return res

    @staticmethod
    def get_or_create_cell(group_id: int, table_name: str, field_name: str, index: int) -> "Cell":
        group = CellGroup.objects.cache().get(id=group_id)
        field = Field.objects.cache().get_or_create(
            table=Table.objects.get(name=table_name, journal=group.journal), name=field_name)[0]

        return Cell.objects.cache().get_or_create(group=group, field=field, index=index)[0]

    class Meta:
        unique_together = ['field', 'index', 'group']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def get_comments_text(self):
        return ''.join(c.get_text() for c in Comment.objects.filter(cell=self))

    @default_if_error(value='')
    def get_responsible_name(self: "Cell"):
        return self.responsible.name


class Comment(models.Model):
    text = models.CharField(max_length=2048, verbose_name='Текст комментария', default='')
    employee = models.ForeignKey('login_app.Employee', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True,
                                     related_name='comments',related_query_name='comment')
    object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('content_type', 'object_id')

    @default_if_error('')
    def get_text(self):
        return self.text
