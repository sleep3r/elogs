from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet

from django.conf import settings
from e_logs.core.utils.webutils import StrAsDictMixin
from e_logs.common.all_journals_app.models import Shift


class Employee(StrAsDictMixin, models.Model):
    POSITION_CHOICES = ( ('master', 'Мастер смены'),
                         ('hydro', 'Аппаратчик'),
                         ('admin', 'Админ'),
                         ('boss', 'Начальник цеха'),
                         ('technologist', 'Технолог цеха'),
                         ('senior technologist', 'Главный технолог'),
                         ('senior master', 'Старший мастер'),
                         ('plant master', 'Мастер цеха'),
                         ('department director', 'Начальник отделения'),
                         ('electrolysis duty', 'Дежурный по электролизу'),
                         )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.CharField(max_length=128, blank=True, choices=POSITION_CHOICES, verbose_name='Должность')
    plant = models.CharField(max_length=128, verbose_name='Цех',
                             null=True, choices=(('furnace', 'Обжиг'),
                                                 ('leaching', 'Выщелачивание'),
                                                 ('electrolysis', 'Электролиз'),
                                                 ))

    @property
    def position_verbose(self):
        return dict(Employee.POSITION_CHOICES)[self.position]

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        indexes = [
            models.Index(fields=['plant', 'position']),
            models.Index(fields=['plant']),
            models.Index(fields=['position']),
        ]

    def unread_messages(self) -> QuerySet:
        from e_logs.common.messages_app.models import Message
        return Message.get_unread(employee=self)
