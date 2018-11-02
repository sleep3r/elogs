import pickle
import pickletools

from typing import Optional, Any

from cacheops import cached_as
from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.auth.models import UserManager
from django.db.models import Q
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models.base import ModelBase

from e_logs.common.all_journals_app.models import Field, Table, Journal, Plant
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.webutils import StrAsDictMixin, logged


class CustomUserManager(UserManager):

    def get_by_natural_key(self, username):
        return self.get(
            Q(**{self.model.USERNAME_FIELD: username}) |
            Q(**{self.model.EMAIL_FIELD: username})
        )


class CustomUser(AbstractUser):
    objects = CustomUserManager()
    REQUIRED_FIELDS = ['email', 'is_superuser', 'user_groups', 'is_boss', 'full_name']

    @property
    def full_name(self):
        return Employee.objects.get(user=self).name

    @property
    def user_groups(self):
        return [group.name for group in self.groups.all()]

    @property
    def is_boss(self):
        if 'validate_cells' in [perm.codename for perm in Permission.objects.filter(user=self)]:
            return [perm.codename for perm in Permission.objects.filter(user=self)]
        else:
            return None


class SettingsMeta(ModelBase):
    @logged
    def __getitem__(self, name: str) -> Any:
        return Setting.get_value(name)

    @logged
    def __setitem__(self, name: str, value) -> None:
        Setting.set_value(name, value)


class TargetedSetting:
    @logged
    def __init__(self, employee: Optional[Employee] = None, obj=None):
        self.obj = obj
        # self.kwargs = kwargs
        self.employee = employee

    @logged
    def __getitem__(self, name: str) -> Any:
        return Setting.get_value(name, obj=self.obj, employee=self.employee)

    @logged
    def __setitem__(self, name: str, value) -> None:
        Setting.set_value(name=name, value=value, employee=self.employee, obj=self.obj)

    def __str__(self):
        return f'TargetedSetting obj={self.obj} kwargs employee={self.employee}'


class Setting(StrAsDictMixin, models.Model, metaclass=SettingsMeta):
    """
    Arbitrary setting for Field/Journal/Table/Plant,
    or any model related to them
    """
    name = models.CharField(max_length=128, verbose_name='Имя')
    verbose_name = models.CharField(max_length=256, verbose_name='Название', blank=True)
    value = models.BinaryField(max_length=4096, verbose_name='Значение')
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE, blank=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
                                     null=True, related_name='settings',
                                     related_query_name='setting', blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    scope = GenericForeignKey('content_type', 'object_id')

    class Meta:
        # equivalent to unique_together = [name, employee, scope], but this works
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
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
    def get_value(name: str, obj=None, employee: Optional[Employee] = None) -> Any:
        """
        Returns setting value for object.

        If object is not field/table/journal/plant,
        get related field/table/journal/plant first
        and than return most close setting.
        """

        qs = Setting.objects.filter(**{
            'name': name,
            'employee': employee,
        })

        @cached_as(qs, extra=obj)
        def _cached_get_value(name: str, obj=None, employee: Optional[Employee] = None):
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
                    return pickle.loads(found_setting.value)
            else:  # case of global setting
                try:
                    found_setting = Setting.objects.get(name=name, employee=employee)
                    return found_setting.val()
                except:  # if haven't found, we'll search father
                    pass

            # if no employee specific setting was found,
            # search for global setting
            if not found_setting and employee:
                return Setting.get_value(name, obj)
            # raise ValueError("No such setting")

        return _cached_get_value(name, obj, employee)

    @staticmethod
    @logged
    def set_value(name: str, value, employee: Employee = None, obj=None) -> None:
        try:
            Setting.objects.create(
                value=Setting._dumps(value),
                name=name,
                employee=employee, object_id=obj.id if obj else None,
                content_type=ContentType.objects.get_for_model(obj) if obj else None)
        except:
            Setting.objects.update_or_create(
                defaults={'value': Setting._dumps(value)},
                name=name,
                employee=employee, object_id=obj.id if obj else None,
                content_type=ContentType.objects.get_for_model(obj) if obj else None)

    @staticmethod
    def _dumps(value):
        return pickletools.optimize(pickle.dumps(value, protocol=pickle.HIGHEST_PROTOCOL))

    def val(self):
        return pickle.loads(self.value)

    @staticmethod
    @logged
    def of(obj=None, employee: Optional[Employee] = None) -> TargetedSetting:
        return TargetedSetting(employee=employee, obj=obj)
