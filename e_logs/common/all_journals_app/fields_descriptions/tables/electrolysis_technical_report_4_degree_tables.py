import json
from datetime import time

from e_logs.core.utils.deep_dict import deep_dict
from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *


 #-----------------Left Table-----------------#
lt = deep_dict()

rows_names_for_db = [
    "zn",
    "zn_mix",
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
        "Zn в отр., г/л",
        "Смеси, г/л",
        "H₂SO₄ отр., г/л",
        "Удельный вес хол-го раствора, г/см³",
        "Удельный вес отр-го раствора, г/см³",
        "Температура смеси, ᵒC",
        "Температура в ваннах, ᵒC",
        "Температура H₂O, ᵒC",
        "Давление H₂O, Па",
        "Давление пара, Па",
        "Сточные воды, Рh",
        "Температура точки 5 ВИУ, ᵒC",
        "Температура точки 6 ВИУ, ᵒC",
        "Температура точки 7 ВИУ, ᵒC"
]

lt.row_names = [{"db": db, "view": view} for db, view in
             zip(rows_names_for_db, rows_names_for_view)]


field_infos_for_rows = [gl_default]*3 + [gsm3_default]*2 +[temperature_default]*3 + [pa_default]*2+[dict(type="number", units = "Рh")]+[temperature_default]*3

lt.times = [
    ":".join(str(time(hour=hour % 24)).split(":")[:-1])
    for hour in range(20, 20 + 12)
]

lt.last_headers = ["mismatches", "measures"]
for row_name, desc in zip(rows_names_for_db, field_infos_for_rows):
    for time in lt.times:
        field_name = row_name + time
        lt[field_name] = desc
    for last in lt.last_headers:
        field_name = row_name + last
        lt[field_name] = text_default

left_table_desc = lt.clear_empty().get_dict()

#-----------------Right Table-----------------#
rt = deep_dict()


rt.h2so4 = text_default
rt.zn = gl_default
rt.viu_in = numeric_default

#--------part1----------#
rt.viu1_1 = m3_default
rt.viu1_2 = m3_default
rt.viu2_1 = m3_default
rt.viu2_2 = m3_default
rt.viu3_1 = m3_default
rt.viu3_2 = m3_default
rt.tank3 = numeric_default
rt.tank4 = numeric_default
rt.tank5 = numeric_default
rt.tank4A = numeric_default
rt.cu1 = mgl_default
rt.co1 = mgl_default
rt.cd1 = mgl_default
rt.sb1 = mgl_default
rt.fe2p1 = mgl_default
rt.bt1 = percent_default
rt.weight1_1 = gsm3_default
rt.weight2_1 = gsm3_default


#--------part2----------#

rt.pumpnum1 = number_default
rt.pumpnum2 = number_default
rt.pumpnum3 = number_default
rt.pumpnum4 = number_default
rt.pumpnum5 = number_default
rt.pumpnum6 = number_default
rt.pumpnum7 = number_default
rt.pumpnum8 = number_default

rt.reason1 = text_default
rt.tank_analisys = number_default
rt.cu2 = mgl_default
rt.co2 = mgl_default
rt.cd2 = mgl_default
rt.sb2 = mgl_default
rt.fe2p2 = mgl_default
rt.weight1_2 = gsm3_default

#--------part3–--------#

rt.pumpnum9 = number_default
rt.pumpnum10 = number_default
rt.pumpnum11 = number_default
rt.pumpnum12 = number_default
rt.reason2 = text_default
rt.pumpnum13 = number_default
rt.pumpnum14 = number_default
rt.pumpnum15 = number_default
rt.pumpnum16 = number_default
rt.pumpnum17 = number_default
rt.pumpnum18 = number_default
rt.reason3 = text_default
rt.zump_pump = number_default
rt.reason4 = text_default


right_table_desc = rt.clear_empty().get_dict()
