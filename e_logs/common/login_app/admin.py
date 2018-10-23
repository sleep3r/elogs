from django.contrib import admin

from e_logs.core.models import CustomUser
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name = 'Профиль'
    verbose_name_plural = 'Профили'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    search_fields = ['username', 'first_name', 'last_name']
    list_display = ['full_name', 'username', 'plant_name', 'position']
    list_display_links = ['full_name']

    @staticmethod
    def full_name(obj):
        return obj.first_name + " " + obj.last_name

    @staticmethod
    def plant_name(obj):
        return obj.employee.plant

    @staticmethod
    def position(obj):
        return obj.employee.position


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    search_fields = ['name']
    list_display = ['name', 'position', 'plant', 'id']
    list_filter = ('position', 'plant')
    list_display_links = ['name']


# Re-register UserAdmin
# admin.site.unregister(User)
admin.site.register(CustomUser, UserAdmin)