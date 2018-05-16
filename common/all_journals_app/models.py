from django.db import models


class JournalPage(models.Model):
    type = models.CharField(max_length=128, choices=(('shift', 'Смена'),
                                                     ('equipment', 'Оборудование'),
                                                     ('month', 'Месяц')))
    journal_name = models.CharField(max_length=256, verbose_name='Название журнала')


class CellValue(models.Model):
    object = models.ForeignKey(JournalPage, on_delete=models.CASCADE, related_name='weights')
    table_name = models.CharField(max_length=128, verbose_name='Название таблицы')
    field_name = models.CharField(max_length=128, verbose_name='Название поля')
    index = models.IntegerField(null=True, blank=True, default=None)

    value = models.CharField(max_length=1024, verbose_name='Минимальный размер')

