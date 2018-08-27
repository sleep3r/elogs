import json

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from django.utils import timezone
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import filter_or_none, get_or_none


class Mode(models.Model):
    is_active = models.BooleanField(default=True)
    message = models.CharField(max_length=512, default='')
    beginning = models.DateTimeField(default=timezone.now)
    end = models.DateTimeField()

    @staticmethod
    def get_active_or_none(field):
        constraint = FieldConstraints.objects.filter(field=field).last()

        if constraint:
            if constraint.mode.is_active == True and constraint.mode.end > timezone.now():
                return constraint.mode
            elif constraint.mode.is_active == True and constraint.mode.end < timezone.now():
                constraint.mode.is_active = False
                constraint.mode.save()

        return None

    class Meta:
        verbose_name = 'Режим'
        verbose_name_plural = 'Режимы'


class FieldConstraints(models.Model):
    min_normal = models.IntegerField()
    max_normal = models.IntegerField()
    field = models.ForeignKey('all_journals_app.Field', on_delete=models.CASCADE)
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE)


    class Meta:
        verbose_name = 'Ограничения для поля'
        verbose_name_plural = 'Ограничения для полей'

