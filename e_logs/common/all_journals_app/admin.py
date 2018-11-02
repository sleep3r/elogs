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

    @staticmethod
    def plant_name(obj):
        return obj.journal.plant.verbose_name


class CellValueAdmin(admin.ModelAdmin):
    model = Cell
    empty_value_display = 'None'
    search_fields = ['table', 'field_name']
    list_display_links = ['field_name']
    list_display = ['id','plant_name','journal_name', 'field_name', 'index', 'value']


    @staticmethod
    def journal_name(obj):
        return obj.group.journal.verbose_name

    @staticmethod
    def plant_name(obj):
        return obj.group.journal.plant.verbose_name

    @staticmethod
    def field_name(obj):
        return obj.field.name


admin.site.register(Cell, CellValueAdmin)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(Plant, PlantAdmin)