from datetime import time, datetime, timedelta, date
from functools import lru_cache

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property
from django.utils.timezone import make_aware

from e_logs.core.utils.webutils import StrAsDictMixin, none_if_error, logged, default_if_error


class Plant(StrAsDictMixin, models.Model):
    name = models.CharField(default='leaching',
                            verbose_name='Название цеха',
                            max_length=128,
                            choices=(('leaching', 'Выщелачивание'),
                                     ('furnace', 'Обжиг'),
                                     ('electrolysis', 'Электролиз')))
    settings = GenericRelation('core.Setting', related_query_name='plant', related_name='plants')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='plant',
                               related_name='plants')

    class Meta:
        verbose_name = 'Цех'
        verbose_name_plural = 'Цеха'


class Journal(StrAsDictMixin, models.Model):
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
    settings = GenericRelation('core.Setting', related_query_name='journal',
                               related_name='journals')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='journal',
                               related_name='journals')

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'


class Table(StrAsDictMixin, models.Model):
    """Abstract table entity."""

    name = models.CharField(max_length=128, verbose_name='Название таблицы')
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE, related_name='tables')
    settings = GenericRelation('core.Setting', related_query_name='table', related_name='tables')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='table',
                               related_name='tables')

    @cached_property
    def plant(self):
        return self.journal.plant

    def cells(self, page):
        return Cell.objects.select_related('field', 'field__table') \
            .filter(group=page, field__table=self)

    def get_fields(self):
        return self.fields.all()

    class Meta:
        verbose_name = 'Таблица'
        verbose_name_plural = 'Таблицы'


class Field(StrAsDictMixin, models.Model):
    """Abstract field entity."""

    name = models.CharField(max_length=128, verbose_name='Название поля')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='fields')
    settings = GenericRelation('core.Setting', related_query_name='field', related_name='fields')
    comments = GenericRelation('all_journals_app.Comment', related_query_name='field',
                               related_name='fields')

    @cached_property
    def plant(self):
        return self.table.journal.plant

    @cached_property
    def journal(self):
        return self.table.journal

    class Meta:
        verbose_name = 'Поле'
        verbose_name_plural = 'Поля'

        indexes = [
            models.Index(fields=['name']),
        ]


class CellGroup(StrAsDictMixin, models.Model):
    journal = models.ForeignKey(Journal, on_delete=models.CASCADE)

    def tables(self):
        return self.journal.tables.all()


class Measurement(CellGroup):
    time = models.DateTimeField(blank=True, null=True, verbose_name='Дата начала смены')


class Shift(CellGroup):
    order = models.IntegerField(verbose_name='Номер смены')
    date = models.DateField(verbose_name='Дата начала смены')

    @property
    def start_time(self) -> timezone.datetime:
        number_of_shifts = Shift.get_number_of_shifts(self.journal)
        shift_hour = (8 + (self.order - 1) * (24 // number_of_shifts)) % 24
        shift_time = time(hour=shift_hour)
        return make_aware(datetime.combine(self.date, shift_time))

    @cached_property
    def end_time(self) -> timezone.datetime:
        number_of_shifts = Shift.get_number_of_shifts(self.journal)
        shift_length = timedelta(hours=24 // number_of_shifts)
        return self.start_time + shift_length

    @property
    def is_active(self) -> bool:
        return self.start_time <= timezone.now() <= self.end_time

    @staticmethod
    @lru_cache(maxsize=1000)
    def get_number_of_shifts(obj):
        # avoiding import loop
        from e_logs.core.models import Setting
        return Setting.of(obj)['number_of_shifts']

    class Meta:
        verbose_name = 'Журнал'
        verbose_name_plural = 'Журналы'

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
                                                    date=date.today())[0]
                if shift.is_active:
                    break

        return shift


class Equipment(CellGroup):
    name = models.CharField(max_length=1024, verbose_name='Название оборудования', default='')


class Cell(StrAsDictMixin, models.Model):
    """Specific cell in some table."""

    group = models.ForeignKey(CellGroup, on_delete=models.CASCADE, related_name='data')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='cells')
    index = models.IntegerField(default=None, verbose_name='Номер строчки')
    value = models.CharField(max_length=1024, verbose_name='Значение поля', blank=True, default='')
    responsible = models.ForeignKey('login_app.Employee', on_delete=models.SET_NULL, null=True)
    comments = GenericRelation('all_journals_app.Comment', related_query_name='cell')

    @cached_property
    def journal(self) -> Journal:
        return self.field.table.journal

    @cached_property
    def table(self) -> Table:
        return self.field.table

    @cached_property
    def name(self) -> str:
        return self.field.name

    @staticmethod
    @none_if_error
    def get_by_addr(field_name, table_name, group_id, index):
        # fixme: not sure if we need this manager
        manager = Cell.objects.select_related('field', 'field__table')
        res = manager.get(field__name=field_name, field__table__name=table_name,
                          group_id=group_id, index=index)
        return res

    @staticmethod
    def get_or_create_cell(group_id: int, table_name: str, field_name: str, index: int) -> "Cell":
        group = CellGroup.objects.get(id=group_id)
        field = Field.objects.get(table__journal=group.journal, table__name=table_name,
                                  name=field_name)
        return Cell.objects.get_or_create(group=group, field=field, index=index)[0]

    class Meta:
        unique_together = ['field', 'index', 'group']
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def get_comments_text(self):
        return ''.join(c.get_text() for c in Comment.objects.filter(cell=self))


class Comment(StrAsDictMixin, models.Model):
    text = models.CharField(max_length=2048, verbose_name='Текст комментария', default='')
    employee = models.ForeignKey('login_app.Employee', on_delete=models.CASCADE)
    created = models.DateTimeField(default=timezone.now)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    target = GenericForeignKey('content_type', 'object_id')

    @default_if_error('')
    def get_text(self):
        return self.text
