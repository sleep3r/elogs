from django.contrib import admin
from e_logs.common.all_journals_app.models import *



class PlantAdmin(admin.ModelAdmin):
    model = Plant
    list_display = ['id','name']
    list_display_links = ['name']


class JournalPageAdmin(admin.ModelAdmin):
    model = JournalPage
    search_fields = ['journal_name', 'equipment']
    list_display = ['type', 'journal_name', 'plant_name', 'shift_order', 'shift_date', 'date', 'year', 'month', 'equipment', 'time', 'id']
    def plant_name(self, obj):
        return obj.plant.name


class CellValueAdmin(admin.ModelAdmin):
    model = JournalPage
    empty_value_display = 'None'
    search_fields = ['table_name', 'field_name' ]
    list_display_links = ['field_name']
    list_display = ['plant_name','journal_name', 'table_name', 'field_name', 'index', 'value', 'id' ]
    # list_select_related = ('journal_page')
    # list_filter = ('journal_name', 'table_name', 'plant_name')

    def journal_name(self, obj):
        return obj.journal_page.journal_name
    def plant_name(self, obj):
        return obj.journal_page.plant.name


class SettingAdmin(admin.ModelAdmin):
    model = Setting
    search_fields = ['name']
    list_display = ['plant', 'journal', 'name','value', 'table', 'cell', 'id',]
    list_display_links = ['name']




admin.site.register(CellValue, CellValueAdmin)
admin.site.register(JournalPage, JournalPageAdmin)
admin.site.register(Plant, PlantAdmin)
admin.site.register(Setting, SettingAdmin)




# class DenserAnalAdmin(admin.ModelAdmin):
#     model = DenserAnal
#     verbose_name_plural = 'Сгустители'
#     list_display = [ 'ph', 'shift_id', 'point', 'sink', 'cu', 'fe', 'time', 'shift', 'journal']
#     list_display_links = ['ph']
#     # list_editable = [ 'point', 'sink', 'time', 'shift', 'journal' ]
#
# class JournalTableAdmin(admin.ModelAdmin):
#     model = JournalTable
#     verbose_name_plural = 'Жарнулы'
#     list_display = [ 'shift', 'time', 'journal']
