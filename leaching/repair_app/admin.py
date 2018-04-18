from django.contrib import admin

# Register your models here.
from leaching.repair_app.models import Equipment, Repairs


class RepairsAdmin(admin.ModelAdmin):
    model = Repairs
    verbose_name_plural = 'Ремонт оборудования'
    list_display = ['date', 'comment', 'name']
    list_display_links = ['name']


class EquipmentAdmin(admin.ModelAdmin):
    model = Repairs
    verbose_name_plural = 'Ремонт оборудования'
    list_display = ['name']
    list_display_links = ['name']


admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Repairs, RepairsAdmin)