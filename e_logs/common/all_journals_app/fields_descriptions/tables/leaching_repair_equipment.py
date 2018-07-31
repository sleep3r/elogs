from django.db import ProgrammingError, OperationalError

from e_logs.common.all_journals_app.models import Shift
from e_logs.core.utils.deep_dict import deep_dict
from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *


rt = deep_dict()

rt.equipment = dict(type="datalist", options=[
            'Агитатор «Манн» №1',
            'Агитатор «Манн» №2',
            'Агитатор «Манн» №3',
            'Сгуститель №1',
            'Сгуститель №2',
            'Сгуститель №3',
            'Питатель ленточный В – 500 мм',
            'Элеватор ЦГ-400 №1',
            'Элеватор ЦГ-400 №2',
            'Транспортер ленточный В – 650 мм',
        ])
rt.date_view = date_default
rt.name_equipment = text_default
rt.date_finish = date_default
rt.volume_text = text_default
rt.fact_time = text_default

leaching_repair_table_desc = rt.clear_empty().get_dict()
