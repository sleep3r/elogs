from datetime import time

from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *
from e_logs.core.utils.deep_dict import DeepDict

# -----------------Left Table-----------------
lt = DeepDict()

rows_names_for_db = [
    "zn",
    "zn_mix",
    "h2so4",
    "solute1",
    "solute2",
    "mixture_temp",
    "bath_temp",
    "temp1",
    "amperage1"
    "amperage2"
]

rows_names_for_view = [
    "Zn в отр., г/л",
    "Смеси, г/л",
    "H₂SO₄ отр., г/л",
    "Температура смеси, ᵒC",
    "Температура в ваннах, ᵒC",
    "Температура нейтр. град., ᵒC",
    "1 серия, кА",
    "2 серия, кА"
]

row_names = [{"db": db, "view": view} for db, view in
                zip(rows_names_for_db, rows_names_for_view)]

field_infos_for_rows = [gl_default] * 3 + [temperature_default] * 3 + [amperage_default] * 2

times = [
    ":".join(str(time(hour=hour % 24)).split(":")[:-1])
    for hour in range(20, 20 + 12)
]

last_headers = ["inconsistencies", "measures"]
for row_name, desc in zip(rows_names_for_db, field_infos_for_rows):
    for time in times:
        field_name = row_name + time
        lt[field_name] = desc
    for last in last_headers:
        field_name = row_name + last
        lt[field_name] = text_default

left_table_desc = lt.clear_empty().get_dict()

lt.grad1_vent = ob_min
lt.grad2_vent = ob_min
lt.grad3_vent = ob_min
lt.grad4_vent = ob_min
lt.grad5_vent = ob_min
lt.grad6_vent = ob_min
lt.grad7_vent = ob_min
lt.grad8_vent = ob_min
lt.grad9_vent = ob_min

lt.grad1_mode = numeric_default
lt.grad2_mode = numeric_default
lt.grad3_mode = numeric_default
lt.grad4_mode = numeric_default
lt.grad5_mode = numeric_default
lt.grad6_mode = numeric_default
lt.grad7_mode = numeric_default
lt.grad8_mode = numeric_default
lt.grad9_mode = numeric_default

lt.crystal1 = numeric_default
lt.crystal2 = numeric_default
lt.common1 = m3_default
lt.common2 = text_default
lt.series31 = m3_default
lt.series32 = text_default
lt.series41 = m3_default
lt.series42 = text_default

lt.pumps_summ = text_default

# -----------------Right Table-----------------#
rt = DeepDict()

rt.h2so4 = text_default
rt.zn = gl_default

# --------part1----------#
rt.solodka = gt_default
rt.glue = gt_default
rt.stroncii = gt_default
rt.magnaflok = gt_default
rt.znk = gt_default
rt.cu1 = mgl_default
rt.co1 = mgl_default
rt.cd1 = mgl_default
rt.sb1 = mgl_default
rt.fe2p1 = mgl_default
rt.bt1 = percent_default
rt.weight1_1 = gsm3_default

rt.glue_resid_up = percent_default
rt.glue_resid_down = percent_default
rt.solodka_resid_up = percent_default
rt.solodka_resid_down = percent_default
rt.magnaflok_resid = kg_default
rt.stroncii_resid = kg_default
rt.cryst1 = numeric_default
rt.cryst2 = numeric_default

right_table_desc = rt.clear_empty().get_dict()
