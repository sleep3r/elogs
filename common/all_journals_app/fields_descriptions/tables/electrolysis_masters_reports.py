from common.all_journals_app.fields_descriptions.fields_classes import date_default, text_default, numeric_default
from utils.deep_dict import deep_dict

lt = deep_dict()

lt.time1 = text_default
lt.time2 = text_default
lt.time3 = text_default
lt.time4 = text_default
lt.defence1 = text_default
lt.defence2 = text_default
lt.defence3 = text_default
lt.defence4 = text_default
lt.weight1 = text_default
lt.passed_fio = text_default
lt.accepted_fio = text_default
lt.sign1 = text_default
lt.sign2 = text_default
lt.sign3 = text_default
lt.sign4 = text_default
lt.weight2 = text_default
lt.passed_sing = text_default
lt.accepted_sign = text_default

last_table_desc = lt.clear_empty().get_dict()

s1 = deep_dict()
s1.h2so4_fact = numeric_default
s1.zn_fact = numeric_default
s1.sm_fact = numeric_default
s1.q_fact = numeric_default
s1.h2so4_nesootv = numeric_default
s1.zn_nesootv = numeric_default
s1.sm_nesootv = numeric_default
s1.q_nesootv = numeric_default
s1.h2so4_mery = text_default
s1.zn_mery = text_default
s1.sm_mery = text_default
s1.q_mery = text_default
s1.h2so4_rosp = text_default
s1.zn_rosp = text_default
s1.sm_rosp = text_default
s1.q_rosp = text_default

s1.gradirni = text_default

seria1_table_desc = s1.clear_empty().get_dict()
seria3_table_desc = s1.clear_empty().get_dict()
seria4_table_desc = s1.clear_empty().get_dict()