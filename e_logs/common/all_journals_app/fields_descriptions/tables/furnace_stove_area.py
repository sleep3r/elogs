from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict

p1t1 = deep_dict()
p1t1.number = number_default
p1t1.rate = m3hour_default
p1t1.elasticity = kgsm2_default
p1t1.rate_o2 = m3hour_default
p1t1.rate_o2_prc = percent_default
p1t1.temperture_in_layer = temperature_default
p1t1.temperture_under = temperature_default
p1t1.volume = m3_default
p1t1.pressure = mmwst_default
p1t1.uio_select = dict(type="datalist", options=['-','Pб', 'Pт', 'Qп'])
p1t1.uio = kgsm2_default
p1t1.smoke = text_default
fa_main_table_desc = p1t1.clear_empty().get_dict()


ut = deep_dict()
ut.ks1 = number_default   # № печи
ut.val1 = tm2_day_default  # значение
ut.ks2 = number_default   # № печи
ut.val2 = tm2_day_default  # значение
ut.ks3 = number_default   # № печи
ut.val3 = tm2_day_default  # значение
udel_table_desc = ut.clear_empty().get_dict()

p1t3 = deep_dict()
p1t3.gmc4_1 = m_default
p1t3.gmc4_2 = m_default
p1t3.gmc1_1 = m_default
p1t3.gmc1_2 = m_default
p1t3.uk3 = m_default
p1t3.uk5 = m_default
p1t3.uk7 = m_default
p1t3.uk4 = m_default
p1t3.uk6 = m_default
p1t3.tonn = ton_default
p1t3.silos1 = m_default
p1t3.silos2 = m_default
p1t3.silos3 = m_default
p1t3.silos4 = m_default
p1t3.silos5 = m_default
p1t3.silos6 = m_default
p1t3.silos7 = m_default
p1t3.silos8 = m_default
p1t3.silos9 = m_default
p1t3.elevators = number_default
p1t3.mills = number_default
p1t3.separators = number_default

page1_table3_desc = p1t3.clear_empty().get_dict()

fences = deep_dict()
fences.results = text_default
fences.term = date_default
fences.mark = text_default
page1_fences_desc = fences.clear_empty().get_dict()


ef = deep_dict()
ef.M_s1_t_in = temperature_default
ef.M_s2_t_in = temperature_default
ef.G_s1_t_in = temperature_default
ef.G_s2_t_in = temperature_default
ef.s1_t_in = temperature_default
ef.s2_t_in = temperature_default
ef.M_s1_t_out = temperature_default
ef.M_s2_t_out = temperature_default
ef.G_s1_t_out = temperature_default
ef.G_s2_t_out = temperature_default
ef.s1_t_out = temperature_default
ef.s2_t_out = temperature_default
ef.M_s1_vam = text_default
ef.M_s2_vam = text_default
ef.G_s1_vam = text_default
ef.G_s2_vam = text_default
ef.s1_vam = text_default
ef.s2_vam = text_default
ef.M_s1_con = percent_default
ef.M_s2_con = percent_default
ef.G_s1_con = percent_default
ef.G_s2_con = percent_default
ef.s1_con = percent_default
ef.s2_con = percent_default
ef.gas1 = text_default
ef.gas2 = text_default
ef.gas3 = text_default
ef.M_s1_fact = m3_default
ef.M_s2_fact = m3_default
ef.G_s1_fact = m3_default
ef.G_s2_fact = m3_default
ef.s1_fact = m3_default
ef.s2_fact = m3_default
ef.vak1 = text_default
ef.vak2 = text_default
electro_filters_desc = ef.clear_empty().get_dict()


wc = deep_dict()
wc.shihta = numeric_default
wc.on_station = numeric_default
wc.unload = numeric_default
wc.r1_per_shift = vmt_default
wc.r1_per_day = vmt_default
wc.r1_unload_shift = pieces_default
wc.r1_unload_day = pieces_default

wc.r2_per_shift = vmt_default
wc.r2_per_day = vmt_default
wc.r2_unload_shift = pieces_default
wc.r2_unload_day = pieces_default

wc.r3_per_shift = vmt_default
wc.r3_per_day = vmt_default
wc.r3_unload_shift = pieces_default
wc.r3_unload_day = pieces_default
wc.crusher_number = number_default
wc.moisture = percent_default
wh_concentrates_desc = wc.clear_empty().get_dict()


am = deep_dict()
am.conc_o2 = percent_default
am.time_start = time_default
am.cnt_in_process = number_default
air_machines_desc = am.clear_empty().get_dict()


p2t1 = deep_dict()
p2t1.time = time_default
p2t1.collector = mm_vod_st_default
p2t1.concentration = percent_default
p2t1.mixture = percent_default
p2t1.conformity = text_default
page2_table1_desc = p2t1.clear_empty().get_dict()


p2t2 = deep_dict()
p2t2.time = time_default
p2t2.place = numeric_default
p2t2.S_cinder = percent_default
p2t2.S_general = percent_default
p2t2.conformity = text_default
p2t2.event = text_default
page2_table2_desc = p2t2.clear_empty().get_dict()


p2t3 = deep_dict()
p2t3.time = time_default
p2t3.character = text_default
p2t3.correction = text_default
p2t3.extra = numeric_default
p2t3.ks_comment = text_default
page2_table3_desc = p2t3.clear_empty().get_dict()


p2t4 = deep_dict()
p2t4.time = time_default
p2t4.comments = text_default
p2t4.mark = text_default
page2_table4_desc = p2t4.clear_empty().get_dict()


p2t5 = deep_dict()
p2t5.material = text_default
p2t5.note = text_default
p2t5.aspiration = text_default
p2t5.kip = text_default
p2t5.electro = text_default
p2t5.extra_note = text_default
page2_table5_desc = p2t5.clear_empty().get_dict()

