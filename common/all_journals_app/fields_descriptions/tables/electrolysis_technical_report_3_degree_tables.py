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
    "temp1",
    "temp2",
]

rows_names_for_view = [
        "Zn в отр./смеси г/л",
        "H2SO4 отр. г/л",
        "Удельный вес хол-го раствора",
        "Удельный вес отр-го раствора",
        "Температура смеси, С",
        "Температура в ваннах, С",
        "Температура 1",
        "Температура 2",
]

lt.row_names = [{"db": db, "view": view} for db, view in
             zip(rows_names_for_db, rows_names_for_view)]


field_infos_for_rows = [numeric_default] * 12 + [text_default] * 2

lt.times = [
    ":".join(str(time(hour=hour % 24)).split(":")[:-1])
    for hour in range(20, 20 + 12)
]

lt.last_headers = ["inconsistencies", "measures"]
for row_name, desc in zip(rows_names_for_db, field_infos_for_rows):
    for time in lt.times + lt.last_headers:
        field_name = row_name + time
        lt[field_name] = desc

left_table_desc = lt.clear_empty().get_dict()

#-----------------Right Table-----------------#
rt = deep_dict()


rt.h2so4 = text_default
rt.zn = text_default

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
rt.znk = numeric_default
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
rt.pumpnum9 = numeric_default
rt.pumpnum10 = numeric_default
rt.pumpnum11 = numeric_default
rt.pumpnum12 = numeric_default
rt.zumppumpnum = numeric_default
rt.shampoopumpnum1 = numeric_default
rt.shampoopumpnum2 = numeric_default
rt.shampoopumpnum3 = numeric_default
rt.reason1 = text_default
rt.reason2 = text_default


right_table_desc = rt.clear_empty().get_dict()
