import json
from utils.deep_dict import deep_dict
from datetime import time
from common.all_journals_app.fields_descriptions.fields_classes import *


 #-----------------Left Table-----------------#
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


field_infos_for_rows = [numeric_default] * 12 + [text_default] * 2

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

#-----------------Right Table-----------------#
rt = deep_dict()


rt.h2so4 = text_default
rt.zn = text_default
rt.viu_in = numeric_default

#--------part1----------#
rt.viu1_1 = numeric_default
rt.viu1_2 = numeric_default
rt.viu2_1 = numeric_default
rt.viu2_2 = numeric_default
rt.viu3_1 = numeric_default
rt.viu3_2 = numeric_default
rt.tank3 = numeric_default
rt.tank4 = numeric_default
rt.tank5 = numeric_default
rt.tank4A = numeric_default
rt.cu1 = numeric_default
rt.co1 = numeric_default
rt.cd1 = numeric_default
rt.sb1 = numeric_default
rt.fe2p1 = numeric_default
rt.bt1 = numeric_default
rt.weight1_1 = numeric_default
rt.weight2_1 = numeric_default


#--------part2----------#

rt.pumpnum1 = numeric_default
rt.pumpnum2 = numeric_default
rt.pumpnum3 = numeric_default
rt.pumpnum4 = numeric_default
rt.pumpnum5 = numeric_default
rt.pumpnum6 = numeric_default
rt.pumpnum7 = numeric_default
rt.pumpnum8 = numeric_default

rt.reason1 = text_default
rt.tank_analisys = numeric_default
rt.cu2 = numeric_default
rt.co2 = numeric_default
rt.cd2 = numeric_default
rt.sb2 = numeric_default
rt.fe2p2 = numeric_default
rt.weight2_1 = numeric_default

#--------part3–--------#

rt.pumpnum9 = numeric_default
rt.pumpnum10 = numeric_default
rt.pumpnum11 = numeric_default
rt.pumpnum12 = numeric_default
rt.reason2 = text_default
rt.pumpnum13 = numeric_default
rt.pumpnum14 = numeric_default
rt.pumpnum15 = numeric_default
rt.pumpnum16 = numeric_default
rt.pumpnum17 = numeric_default
rt.pumpnum18 = numeric_default

rt.reason3 = text_default
rt.reason3 = text_default

right_table_desc = rt.clear_empty().get_dict()
