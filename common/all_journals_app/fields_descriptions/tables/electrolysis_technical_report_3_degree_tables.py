import json
from utils.deep_dict import deep_dict
from datetime import time
from common.all_journals_app.fields_descriptions.fields_classes import *


 #-----------------Left Table-----------------#
lt = deep_dict()

rows_names_for_db = [
    "zn",
    "zn_mix"
    "h2so4",
    "solute1",
    "solute2",
    "mixture_temp",
    "bath_temp",
    "temp1",
    "temp2",
]

rows_names_for_view = [
        "Zn в отр., г/л",
        "Смеси, г/л",
        "H₂SO₄ отр., г/л",
        "Удельный вес хол-го раствора, г/см³",
        "Удельный вес отр-го раствора, г/см³",
        "Температура смеси, ᵒC",
        "Температура в ваннах, ᵒC",
        "Температура 1, ᵒC",
        "Температура 2, ᵒC",
]

lt.row_names = [{"db": db, "view": view} for db, view in
             zip(rows_names_for_db, rows_names_for_view)]


field_infos_for_rows = [gl_default]*3 + [gsm3_default]*2+[temperature_default]*4

lt.times = [
    ":".join(str(time(hour=hour % 24)).split(":")[:-1])
    for hour in range(20, 20 + 12)
]

lt.last_headers = ["inconsistencies", "measures"]
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

#--------part1----------#
rt.grad1_1 = numeric_default
rt.grad1_2 = numeric_default
rt.grad2_1 = numeric_default
rt.grad2_2 = numeric_default
rt.tank1_1 = numeric_default
rt.tank1_2 = numeric_default
rt.tank2_1 = numeric_default
rt.tank2_2 = numeric_default
rt.cons1 = numeric_default
rt.cons2 = numeric_default
rt.znk = ton_default
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
rt.pumpnum9 = number_default
rt.pumpnum10 = number_default
rt.pumpnum11 = number_default
rt.pumpnum12 = number_default
rt.zumppumpnum = number_default
rt.shampoopumpnum1 = number_default
rt.shampoopumpnum2 = number_default
rt.shampoopumpnum3 = number_default
rt.reason1 = text_default
rt.reason2 = text_default


right_table_desc = rt.clear_empty().get_dict()
