import json
from utils.deep_dict import deep_dict
from datetime import time


lt = deep_dict()

rows_names_for_db = [
    "zn",
    "h2so4",
    "solute1",
    "solute2",
    "mixture_temp",
    "bath_temp",
    "h2o_temp",
    "h2o_pressure",
    "gas_pressure",
    "wastewater",
    "point5_temp",
    "point6_temp",
    "point7_temp"
]

rows_names_for_view = [
        "Zn в отр./смеси г/л",
        "H2SO4 отр. г/л",
        "Удельный вес хол-го раствора",
        "Удельный вес отр-го раствора",
        "Температура смеси, С",
        "Температура в ваннах, С",
        "Температура H2O",
        "Давление H2O",
        "Давление пара",
        "Сточные воды, Рн",
        "Температура точки 5 ВИУ, С",
        "Температура точки 6 ВИУ, С",
        "Температура точки 7 ВИУ, С"
]

lt.row_names = [{"db": db, "view": view} for db, view in
             zip(rows_names_for_db, rows_names_for_view)]


field_infos_for_rows = [
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='number', min_normal=10, max_normal=1000),
    dict(type='text', min_normal=10, max_normal=1000),
    dict(type='text', min_normal=10, max_normal=1000),
]

lt.times = [
    ":".join(str(time(hour=hour % 24)).split(":")[:-1])
    for hour in range(20, 20 + 12)
]

lt.last_headers = ["mismatches", "measures"]
for row_name, desc in zip(rows_names_for_db, field_infos_for_rows):
    for time in lt.times + lt.last_headers:
        field_name = row_name + time
        lt[field_name] = desc

left_table_desc = lt.clear_empty().get_dict()
