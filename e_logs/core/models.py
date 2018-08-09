from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from e_logs.common.all_journals_app.models import Field, Table, Journal, Plant
from e_logs.common.login_app.models import Employee


class Setting(models.Model):
    """
    Arbitrary setting for Field/Journal/Table/Plant,
    or any model related to them
    """
    name = models.CharField(max_length=128, verbose_name='Название')
    value = models.CharField(max_length=2048, verbose_name='Значение')
    employee = models.ForeignKey(Employee, null=True, on_delete=models.CASCADE)

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True
    )
    object_id = models.PositiveIntegerField(null=True)
    scope = GenericForeignKey('content_type', 'object_id')

    # equivalent to unique_together = [name, employee, scope], but this works
    class Meta:
        unique_together = (('name', 'employee', 'content_type', 'object_id'),)

    @staticmethod
    def get_value(name, obj=None, employee=None):
        """
        Returns setting value for object.

        If object is not field/table/journal/plant,
        get related field/table/journal/plant first
        and than return most close setting.
        """
        scopes_attrs = (
            (Field, 'field'),
            (Table, 'table'),
            (Journal, 'journal'),
            (Plant, 'plant'),
        )
        found_setting = None
        for (scope, attr) in scopes_attrs:
            # get parent object if it exists
            if hasattr(obj, attr):
                obj = getattr(obj, attr)
            if type(obj) == scope:
                found_setting = Setting.objects.filter(**{
                                    'name': name,
                                    'employee': employee,
                                    attr: obj
                                }).first()
            if found_setting:
                return found_setting.value
        # if no employee specific setting was found,
        # search for global setting
        if not found_setting and employee:
            return Setting.get_value(name, obj)
        raise ValueError("No such setting")
