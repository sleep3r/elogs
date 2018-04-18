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
