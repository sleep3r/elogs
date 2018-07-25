from django.contrib import admin
from e_logs.common.all_journals_app.models import *



class PlantAdmin(admin.ModelAdmin):
    model = Plant
    list_display = ['id','name']
    list_display_links = ['name']


admin.site.register(CellValue)
admin.site.register(JournalPage)
admin.site.register(Plant, PlantAdmin)
admin.site.register(Setting)




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
