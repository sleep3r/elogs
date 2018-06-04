from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from main_app.models import *


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton


class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Department)
admin.site.register(Conference)
admin.site.register(Talker)
admin.site.register(Track)
