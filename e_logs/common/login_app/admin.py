from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )
    search_fields = ['username', 'first_name', 'last_name']
    list_display = ['full_name','username', 'plant_name', 'position' ]
    list_display_links = ['full_name']

    def full_name(self, obj):
        return obj.first_name + " " + obj.last_name

    def plant_name(self, obj):
        return obj.employee.plant

    def position(self, obj):
        return obj.employee.position


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
    search_fields = ['name']
    list_display = ['name', 'position', 'plant', 'csrf', 'id']
    list_filter = ('position', 'plant')
    list_display_links = ['name']


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Employee, EmployeeAdmin)
