from django.contrib import admin
from common.messages_app.models import Message
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class MessageAdmin(admin.ModelAdmin):
    model = Message
    verbose_name_plural = 'Сообщения'
    list_display = ['id', 'is_read', 'text', 'type',  'addressee']
    list_display_links = ['text']
    list_editable = ['addressee', 'is_read']



# Re-register UserAdmin
admin.site.register(Message, MessageAdmin)
