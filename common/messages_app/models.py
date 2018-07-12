from django.contrib.auth.models import User
from django.db import models
from login_app.models import Employee

from utils.settings import CSRF_LENGTH

class Message(models.Model):
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    text = models.TextField(verbose_name='Текст сообщения')
    type = models.CharField(max_length=100, verbose_name='Тип сообщения', null=True,
                            choices=(('critical_value', 'Критическое значение'),
                                     ('comment', 'Замечание'))
                            )

    addressee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')

    cell_field_name = models.CharField(max_length=128, verbose_name='Название поля ячейки', null = True, default=None)
    cell_table_name = models.CharField(max_length=128, verbose_name='Название таблицы ячейки', null = True, default=None)
    cell_journal_page = models.IntegerField(null=True, blank=True, default=None, verbose_name='Номер журнала ячейки')
    row_index = models.IntegerField(null=True, blank=True, default=None, verbose_name='Номер строчки ячейки')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
