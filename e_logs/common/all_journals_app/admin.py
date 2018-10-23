# from django.contrib import admin
# from e_logs.common.all_journals_app.models import *
# from e_logs.core.models import Setting
#
#
# class PlantAdmin(admin.ModelAdmin):
#     model = Plant
#     list_display = ['id', 'name']
#     list_display_links = ['name']
#
#
# class JournalPageAdmin(admin.ModelAdmin):
#     model = Shift
#     search_fields = ['name', 'equipment']
#     list_display = ['plant_name', 'order', 'date', 'id']
#
#     @staticmethod
#     def plant_name(obj):
#         return obj.plant.name
#
#
# class CellValueAdmin(admin.ModelAdmin):
#     model = Cell
#     empty_value_display = 'None'
#     search_fields = ['table', 'field']
#     list_display_links = ['field']
#     list_display = ['group', 'field', 'index', 'value', 'id']
#
#     # list_select_related = ('journal_page')
#     # list_filter = ('journal_name', 'table_name', 'plant_name')
#
#     @staticmethod
#     def journal_name(obj):
#         return obj.journal_page.group
#
#     @staticmethod
#     def plant_name(obj):
#         return obj.journal_page.plant.name
#
#
# class SettingAdmin(admin.ModelAdmin):
#     model = Setting
#     search_fields = ['name']
#     list_display = ['scope', 'name', 'value', 'id', ]
#     list_display_links = ['name']
#
#
# admin.site.register(Cell, CellValueAdmin)
# admin.site.register(Shift, JournalPageAdmin)
# admin.site.register(Plant, PlantAdmin)
# admin.site.register(Setting, SettingAdmin)
#
# # class DenserAnalAdmin(admin.ModelAdmin):
# #     model = DenserAnal
# #     verbose_name_plural = 'Сгустители'
# #     list_display = [ 'ph', 'shift_id', 'point', 'sink', 'cu', 'fe', 'time', 'shift', 'journal']
# #     list_display_links = ['ph']
# #     # list_editable = [ 'point', 'sink', 'time', 'shift', 'journal' ]
# #
# # class JournalTableAdmin(admin.ModelAdmin):
# #     model = JournalTable
# #     verbose_name_plural = 'Жарнулы'
# #     list_display = [ 'shift', 'time', 'journal']
