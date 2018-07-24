from django.db import models

class Feedback(models.Model):
    theme = models.CharField(max_length=200, verbose_name='Тема')
    text = models.CharField(max_length=1000, verbose_name='Сообщение')
    plant = models.CharField(max_length=50, verbose_name='Цех')
    journal = models.CharField(max_length=256, verbose_name="Журнал")
    email = models.CharField(max_length=200, verbose_name='Почта')
    username = models.CharField(max_length=200, blank=True, null=True, verbose_name='Пользователь')
