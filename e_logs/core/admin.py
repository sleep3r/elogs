from django.contrib import admin
from django.contrib.auth.models import Group
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule, SolarSchedule
from rest_framework.authtoken.models import Token
from e_logs.core.models import Setting

admin.site.unregister(TaskResult)
admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(Token)
admin.site.unregister(Group)


class SettingsAdmin(admin.ModelAdmin):
    model = Setting
    verbose_name_plural = 'Настройки'
    list_display = ['id', 'name', 'verbose_name', 'value']
    list_display_links = ['name']
    # list_editable = ['value',]

admin.site.register(Setting, SettingsAdmin)
