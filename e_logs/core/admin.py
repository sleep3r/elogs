from django.contrib import admin
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule, SolarSchedule
from rest_framework.authtoken.models import Token

admin.site.unregister(TaskResult)
admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(Token)