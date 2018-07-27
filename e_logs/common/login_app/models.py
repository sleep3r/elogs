from django.contrib.auth.models import User
from django.db import models
from e_logs.common.all_journals_app.models import Cell, JournalPage

from e_logs.core.utils.settings import CSRF_LENGTH


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    position = models.CharField(max_length=128, blank=True, choices=(('master', 'Мастер'),
                                                                     ('laborant', 'Лаборант'),
                                                                     ('hydro', 'Аппаратчик-гидрометаллург'),
                                                                     ('admin', 'Админ'),
                                                                     ('boss', 'Начальник цеха'),
                                                                     ))
    plant = models.CharField(max_length=128, verbose_name='Цех', null=True, choices=(('furnace', 'Обжиг'),
                                                                                    ('leaching', 'Выщелачивание'),
                                                                                    ('electrolysis', 'Электролиз'),
                                                                                    ))
    csrf = models.CharField(max_length=CSRF_LENGTH, default=' ')
    owned_journal_pages = models.ManyToManyField(JournalPage, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рабочий'
        verbose_name_plural = 'Рабочие'
