from typing import Optional

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase

from e_logs.common.all_journals_app.models import Field, Table, Journal, Plant
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import StrAsDictMixin, logged
from e_logs.core.utils.loggers import default_logger


class SettingsMeta(ModelBase):
    @logged
    def __getitem__(self, name: str) -> str:
        return Setting.get_value(name)

    @logged
    def __setitem__(self, name: str, value: str) -> None:
        Setting.set_value(name, value)


class TargetedSetting:
    @logged
    def __init__(self, employee: Optional[Employee] = None, obj=None, **kwargs):
        self.obj = obj
        self.kwargs = kwargs
        self.employee = employee

    @logged
    def __getitem__(self, name: str) -> str:
        return Setting.get_value(name, obj=self.obj, employee=self.employee)

    @logged
    def __setitem__(self, name: str, value: str) -> None:
        default_logger.debug(f'self.kwargs={self.kwargs}')
        Setting.set_value(name=name, value=value, employee=self.employee, **self.kwargs)

    def __str__(self):
        return f'TargetedSetting obj={self.obj} kwargs={self.kwargs} employee={self.employee}'


class Setting(StrAsDictMixin, models.Model, metaclass=SettingsMeta):
    """
    Arbitrary setting for Field/Journal/Table/Plant,
    or any model related to them
    """
    name = models.CharField(max_length=128, verbose_name='Название')
    value = models.CharField(max_length=2048, verbose_name='Значение')
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    scope = GenericForeignKey('content_type', 'object_id')

    class Meta:
        # equivalent to unique_together = [name, employee, scope], but this works
        unique_together = (('name', 'employee', 'content_type', 'object_id'),)
        indexes = [
            models.Index(fields=['name', 'employee']),
            models.Index(fields=['name']),
            models.Index(fields=['name', 'content_type', 'object_id']),
        ]

    scopes_attrs = (
        (Field, 'field'),
        (Table, 'table'),
        (Journal, 'journal'),
        (Plant, 'plant'),
    )

    @staticmethod
    @logged
    def get_value(name: str, obj=None, employee: Optional[Employee] = None) -> str:
        """
        Returns setting value for object.

        If object is not field/table/journal/plant,
        get related field/table/journal/plant first
        and than return most close setting.
        """
        found_setting = None
        for (scope, attr) in Setting.scopes_attrs:
            if hasattr(obj, attr):  # get parent object if it exists
                obj = getattr(obj, attr)
            if type(obj) == scope:
                found_setting = Setting.objects.filter(**{
                    'name': name,
                    'employee': employee,
                    attr: obj
                }).first()
            if found_setting:
                return found_setting.value
        else:  # case of global setting
            try:
                found_setting = Setting.objects.get(name=name, employee=employee)
                return found_setting.value
            except:  # if haven't found, we'll search father
                pass

        # if no employee specific setting was found,
        # search for global setting
        if not found_setting and employee:
            return Setting.get_value(name, obj)
        raise ValueError("No such setting")

    @staticmethod
    @logged
    def set_value(name: str, value: str, employee: Employee = None, scope=None, **kwargs) -> None:
        default_logger.debug(f'Set value: {kwargs}')
        try:
            Setting(value=value, name=name, employee=employee, scope=scope).save()
        except:
            Setting.objects.update_or_create(defaults={'value': value}, name=name,
                                             employee=employee, **kwargs)

    @staticmethod
    @logged
    def of(employee: Optional[Employee] = None, **kwargs) -> TargetedSetting:
        default_logger.debug(f'of(kwargs={kwargs})')
        return TargetedSetting(employee=employee, **kwargs)