from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from config.settings.settings_base import CSRF_LENGTH
from e_logs.common.all_journals_app.models import Cell, Shift
from e_logs.core.utils.webutils import StrAsDictMixin


class Employee(StrAsDictMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.CharField(max_length=128,
                                blank=True, choices=(('master', 'Мастер'),
                                                     ('laborant', 'Лаборант'),
                                                     ('hydro', 'Аппаратчик-гидрометаллург'),
                                                     ('admin', 'Админ'),
                                                     ('boss', 'Начальник цеха'),
                                                     ))
    plant = models.CharField(max_length=128, verbose_name='Цех',
                             null=True, choices=(('furnace', 'Обжиг'),
                                                 ('leaching', 'Выщелачивание'),
                                                 ('electrolysis', 'Электролиз'),
                                                 ))
    csrf = models.CharField(max_length=CSRF_LENGTH, default=' ')
    owned_shifts = models.ManyToManyField(Shift, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рабочий'
        verbose_name_plural = 'Рабочие'
        indexes = [
            models.Index(fields=['plant', 'position']),
            models.Index(fields=['plant']),
            models.Index(fields=['position']),
        ]

    def unread_messages(self) -> QuerySet:
        from e_logs.common.messages_app.models import Message
        return Message.get_unread(employee=self)
