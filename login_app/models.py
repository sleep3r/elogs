from django.contrib.auth.models import User
from django.db import models

from utils.settings import CSRF_LENGTH


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.CharField(max_length=128, blank=True, choices=(('master', 'Мастер'),
                                                                     ('laborant', 'Лаборант'),
                                                                     ('hydro', 'Аппаратчик-гидрометаллург'),
                                                                     ('admin', 'Админ'),
                                                                     ('boss', 'Начальник цеха'),
                                                                     ))
    plant = models.CharField(max_length=10, verbose_name='Цех', null=True, choices=(('furnace', 'Обжиг'),
                                                                                    ('leaching', 'Выщелачивание'),
                                                                                    ('electrolysis', 'Электролиз'),
                                                                                    ))
    csrf = models.CharField(max_length=CSRF_LENGTH, default='')

    def __str__(self):
        return f'{self.name}'


class Message(models.Model):
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    text = models.TextField(verbose_name='Текст сообщения')
    type = models.CharField(max_length=100, verbose_name='Тип сообщения', null=True,
                            choices=(('critical_value', 'Критическое значение'),
                                     ('note', 'Замечание'))
                            )

    addressee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
