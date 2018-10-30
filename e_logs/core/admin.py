import pickle

from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType
from django_celery_results.models import TaskResult
from django_celery_beat.models import PeriodicTask, CrontabSchedule, IntervalSchedule, SolarSchedule
from rest_framework.authtoken.models import Token

from e_logs.common.login_app.models import Employee
from e_logs.core.models import Setting


admin.site.unregister(TaskResult)
admin.site.unregister(PeriodicTask)
admin.site.unregister(CrontabSchedule)
admin.site.unregister(IntervalSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(Token)
admin.site.unregister(Group)


class YourModelForm(forms.ModelForm):
    pickled_value = forms.CharField(label='Значение')

    def save(self, commit=True):
        value = self.data.get('pickled_value', None)
        name = self.data.get('name', None)
        employee_id = self.data.get('employee', None)
        content_type_id = self.data.get('content_type', None)
        object_id = self.data.get('object_id', None)

        if name:
            print(self.data)
            if content_type_id and object_id:
                ct = ContentType.objects.get_for_id(content_type_id)
                object = ct.get_object_for_this_type(pk=object_id)
            else:
                object = None

            Setting.set_value(name=name,
                              value=value,
                              employee=Employee.objects.get(id=employee_id) if employee_id else None,
                              obj=object if object else None)

        return super().save(commit=commit)

    class Meta:
        model = Setting
        fields = '__all__'


class SettingsAdmin(admin.ModelAdmin):
    form = YourModelForm
    model = Setting
    verbose_name_plural = 'Настройки'
    list_display = ['id', 'name', 'verbose_name', 'pickled_value']
    list_display_links = ['name']

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        form.base_fields['pickled_value'].initial = self.pickled_value(obj)
        return form

    def pickled_value(self, obj):
        value = pickle.loads(obj.value)
        return value
    pickled_value.short_description = "Значение"


admin.site.register(Setting, SettingsAdmin)
