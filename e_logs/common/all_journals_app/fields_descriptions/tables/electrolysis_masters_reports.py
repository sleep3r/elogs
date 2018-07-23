from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *
from e_logs.core.utils.deep_dict import deep_dict

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
lt.weight2 = text_default
lt.passed_sing = text_default

last_table_desc = lt.clear_empty().get_dict()

s1 = deep_dict()
s3 = deep_dict()
s4 = deep_dict()

s1.h2so4_fact = numeric_default
s1.zn_fact = numeric_default
s1.t_sm_fact = temperature_default
s1.q_fact = numeric_default
s1.h2so4_nesootv = numeric_default
s1.zn_nesootv = numeric_default
s1.t_sm_nesootv = temperature_default
s1.q_nesootv = numeric_default
s1.h2so4_mery = text_default
s1.zn_mery = text_default
s1.t_sm_mery = numeric_default
s1.q_mery = text_default
s1.h2so4_rosp = text_default
s1.zn_rosp = text_default
s1.t_sm_rosp = numeric_default
s1.q_rosp = text_default
s1.gradirni = text_default
s1.cooler1 = number_default
s1.cooler2 = number_default
s1.cooler3 = number_default
s1.cooler4 = number_default
s1.cooler5 = number_default
s1.cooler6 = number_default
s1.cooler7 = number_default
s1.cooler8 = number_default
s1.t_otr_fact = temperature_default
s1.t_otr_nesootv = temperature_default
s1.t_otr_mery = numeric_default
s1.t_otr_rosp = numeric_default

s1.cu = mgl_default
s1.co = mgl_default
s1.sb = mgl_default
s1.fe = mgl_default
s1.cd = mgl_default
s1.t_n = temperature_default
s1.t_gr = temperature_default
s1.V1 = m3_default
s1.V2 = m3_default
s1.V3 = m3_default
s1.V4 = m3_default
s1.V5 = m3_default
s1.V6 = m3_default
s1.V6_otr = m3_default
s1.VII = m3_default


pt = deep_dict()
pt.percent_Pb = percent_default
pt.percent_Cu = percent_default
pt.percent_Fe = percent_default
pt.percent_Cd = percent_default
pt.percent_Al = percent_default
pt.percent_Zn = percent_default


a1 = deep_dict()
a1.col1 = numeric_default
a1.col2 = numeric_default
a1.col3 = numeric_default
a1.col4 = numeric_default
a1.col5 = numeric_default
a1.col6 = numeric_default
a1.desc = text_default

a2 = deep_dict()
a2.col1 = numeric_default
a2.col2 = numeric_default
a2.col3 = numeric_default
a2.col4 = numeric_default
a2.col5 = numeric_default
a2.col6 = numeric_default
a2.desc = text_default
a2.dust = text_default
a2.bunkers = text_default

zt = deep_dict()
zt.zn1 = numeric_default
zt.zn2 = numeric_default
zt.zn3 = numeric_default
zt.zn4 = numeric_default
zt.zn5 = numeric_default
zt.zn6 = numeric_default
zt.zn8 = numeric_default
zt.zn9 = numeric_default
zt.zn10 = numeric_default

zt.skd1 = numeric_default
zt.skd2 = numeric_default
zt.skd3 = numeric_default
zt.skd4 = numeric_default
zt.skd5 = numeric_default
zt.skd6 = numeric_default
zt.skd7 = numeric_default
zt.skd8 = numeric_default

zt.sk1 = numeric_default
zt.sk2 = numeric_default
zt.sk3 = numeric_default
zt.sk4 = numeric_default
zt.sk5 = numeric_default
zt.sk6 = numeric_default
zt.sk7 = numeric_default
zt.sk8 = numeric_default

seria1_table_desc = s1.clear_empty().get_dict()
seria3_table_desc = s1.clear_empty().get_dict()
seria4_table_desc = s1.clear_empty().get_dict()
params_table_desc = pt.clear_empty().get_dict()
melt_area1_table_desc = a1.clear_empty().get_dict()
melt_area2_table_desc = a2.clear_empty().get_dict()
zinc_table_desc = zt.clear_empty().get_dict()
