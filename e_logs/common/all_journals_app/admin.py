from django.contrib import admin
from e_logs.common.all_journals_app.models import *
from e_logs.core.models import Setting


class PlantAdmin(admin.ModelAdmin):
    model = Plant
    list_display = ['id', 'name']
    list_display_links = ['name']


class ShiftAdmin(admin.ModelAdmin):
    model = Shift
    search_fields = ['name', 'equipment']
    list_display = ['plant_name', 'order', 'date', 'id']

    def plant_name(self, obj):
        return obj.journal.plant.verbose_name
    plant_name.short_description = "Цех"


class CellValueAdmin(admin.ModelAdmin):
    model = Cell
    empty_value_display = 'None'
    search_fields = ['table', 'field_name']
    list_display_links = ['field_name']
    list_display = ['id','plant_name','journal_name', 'field_name', 'index', 'value']

    def journal_name(self, obj):
        return obj.group.journal.verbose_name
    journal_name.short_description = "Журнал"

    def plant_name(self, obj):
        return obj.group.journal.plant.verbose_name
    plant_name.short_description = "Цех"

    def field_name(self, obj):
        return obj.field.name
    field_name.short_description = "Поле"

admin.site.register(Cell, CellValueAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Plant, PlantAdmin)