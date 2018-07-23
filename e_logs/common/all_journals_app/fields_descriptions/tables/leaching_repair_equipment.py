from django.db import ProgrammingError, OperationalError

from e_logs.common.all_journals_app.models import JournalPage
from e_logs.core.utils.deep_dict import deep_dict
from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *


def get_equipent():
    try:
        equipments = [item.equipment for item in JournalPage.objects.filter(type='equipment').exclude(equipment__isnull=True)]
    except (ProgrammingError, OperationalError):
        return
    return equipments


rt = deep_dict()

rt.equipment = dict(type="datalist", options=get_equipent())
rt.date_view = date_default
rt.name_equipment = text_default
rt.date_finish = date_default
rt.volume_text = text_default
rt.fact_time = text_default

leaching_repair_table_desc = rt.clear_empty().get_dict()
