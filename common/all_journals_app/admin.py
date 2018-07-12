from django.contrib import admin
from common.all_journals_app.models import *
from guardian.admin import GuardedModelAdmin


class JournalPageAdmin(GuardedModelAdmin):
    pass


admin.site.register(CellValue)
admin.site.register(JournalPage, JournalPageAdmin)
admin.site.register(Plant)
