from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from leaching.express_anal_app.models import *


class DenserAnalAdmin(admin.ModelAdmin):
    model = DenserAnal
    verbose_name_plural = 'Сгустители'
    list_display = [ 'ph', 'cu', 'fe', 'liq_sol','shift_id', 'point', 'sink', 'time', 'shift', 'journal', ]
    list_display_links = ['ph']
    # list_editable = [ 'point', 'sink', 'time', 'shift', 'journal' ]


class JournalTableAdmin(admin.ModelAdmin):
    model = JournalTable
    verbose_name_plural = 'Жарнулы'
    list_display = [ 'shift', 'time', 'journal']


class ShiftAdmin(admin.ModelAdmin):
    model = Shift
    verbose_name_plural = 'Смены'
    list_display = [ 'date', 'order', 'plant', 'master', 'laborant']


class HydroMetalAdmin(admin.ModelAdmin):
    model = HydroMetal
    verbose_name_plural = 'Гидрометаллург'
    list_display = [ 'mann_num', 'ph', 'acid', 'fe2', 'fe_total','cu','sb', 'sediment', 'employee']


admin.site.register(LeachingExpressAnal)
admin.site.register(Journal)
admin.site.register(Shift, ShiftAdmin)
admin.site.register(JournalTable, JournalTableAdmin)
admin.site.register(DenserAnal, DenserAnalAdmin)
admin.site.register(HydroMetal, HydroMetalAdmin)
admin.site.register(CinderDensity)
admin.site.register(SelfSecurity)
admin.site.register(ProductionError)
admin.site.register(ZnPulpAnal)
admin.site.register(CuPulpAnal)
admin.site.register(FeSolutionAnal)
admin.site.register(DailyAnalysis)
admin.site.register(Agitators)
admin.site.register(NeutralDenser)
admin.site.register(ReadyProduct)
admin.site.register(Reagents)
admin.site.register(VEU)
admin.site.register(Sample2)
admin.site.register(FreeTank)
admin.site.register(Electrolysis)
admin.site.register(ShiftInfo)
admin.site.register(Schieht)
admin.site.register(NeutralSolution)
admin.site.register(Cinder)
