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


class MessageAdmin(admin.ModelAdmin):
    model = Message
    verbose_name_plural = 'Сообщения'
    list_display = ['id', 'is_read', 'text', 'type',  'addressee']
    list_display_links = ['text']
    list_editable = ['addressee', 'is_read']



# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Employee)
admin.site.register(Message, MessageAdmin)