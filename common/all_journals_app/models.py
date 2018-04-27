from django.db import models


class Objects(models.Model):
    type = models.CharField(max_length=128, choices=(('shift', 'Смена'),
                                              ('equipment', 'Оборудование'),
                                              ('month', 'Месяц')))


class Values(models.Model):
    object = models.ForeignKey(Objects, on_delete=models.CASCADE, related_name='weights')
    journal_name = models.CharField(max_length=256, verbose_name='Название журнала')
    table_name = models.CharField(max_length=128, verbose_name='Название таблицы')
    field_id = models.CharField(max_length=128, verbose_name='Название поля')
    index = models.IntegerField(null=True, blank=True, default=None)

    value = models.CharField(max_length=1024, verbose_name='Минимальный размер')