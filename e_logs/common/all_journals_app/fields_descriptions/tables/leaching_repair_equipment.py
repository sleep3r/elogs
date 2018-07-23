from django.db import ProgrammingError, OperationalError

from e_logs.leaching.repair_reports_app.models import Equipment
from e_logs.core.utils.deep_dict import deep_dict
from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *


def get_equipent():
    try:
        items = Equipment.objects.all().order_by('name')
        equipments = []
        for item in items:
            equipments.append(item.name)
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
