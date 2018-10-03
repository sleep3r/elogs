import json

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from e_logs.common.all_journals_app.models import Journal
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import filter_or_none, get_or_none


class Mode(models.Model):
    is_active = models.BooleanField(default=False)
    message = models.CharField(max_length=512, default='')
    beginning = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField(null=True)
    journal = models.ForeignKey("all_journals_app.Journal", on_delete=models.CASCADE, null=True)

    @staticmethod
    def get_active_constraint(field, journal):
        mode = get_or_none(Mode, journal=journal)

        if mode and mode.is_active == True:
            constraint = FieldConstraints.objects.filter(field=field, mode=mode).last()

            if constraint:
                return constraint

        return None

    class Meta:
        verbose_name = 'Режим'
        verbose_name_plural = 'Режимы'


class FieldConstraints(models.Model):
    min_normal = models.IntegerField(default=0)
    max_normal = models.IntegerField(default=1000)
    field = models.ForeignKey('all_journals_app.Field', on_delete=models.CASCADE)
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Ограничения для поля'
        verbose_name_plural = 'Ограничения для полей'