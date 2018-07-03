from utils.deep_dict import deep_dict
from common.all_journals_app.fields_descriptions.fields_classes import *



#------year plan schieht--------
yps = deep_dict()
yps.concentrate = dict(type="datalist",options=["ЗГОК", "Арт-ий",
                                                        "Усть-ТАЛ",
                                                        "Карагайлы",
                                                        "Верх-Бер",
                                                        "Белоусовка",
                                                        "Жезкент",
                                                        "Н.Широкинский",
                                                        "Лесосиб",
                                                        "Алтын-Топкан"])
yps.year_plans = smt_default
yps.month_smt = smt_default
yps.day_smt = smt_default
yps.tonns_a_year = ton_default
yps.schieht_frac = percent_default
yps.empty_field = text_default
yps.zn = percent_default
yps.s = percent_default
yps.h2o = percent_default
yps.fe = percent_default
yps.cu = percent_default
yps.pb = percent_default
yps.sio2 = percent_default
yps.cd = percent_default
yps.cao = percent_default
yps.mgo = percent_default
yps.K = percent_default
yps.na = percent_default
yps.arsenic = percent_default
yps.co = percent_default
yps.au = gt_default
yps.ag = gt_default
yps.vmt = vmt_default
yps.norm = dict(type='number', min_normal=10, max_normal=1000)
year_plan_schieht_desc = yps.clear_empty().get_dict()

bt = deep_dict()

#------ Loading Schieht Table --------

main_table = deep_dict()
main_table.concentrate = dict(type="number", min_normal=10, max_normal=1000)
main_table.zn = dict(type="number", min_normal=10, max_normal=1000, units='')
main_table.ratio = dict(type="number", min_normal=10, max_normal=1000, units='')
main_table_desc = main_table.clear_empty().get_dict()


#----- Supply of zinc concentrates table ----
supply_zinc = deep_dict()
supply_zinc.concentrate = smt_default
supply_zinc.zn = dict(type="number", min_normal=10, max_normal=10000)
supply_zinc_desc = supply_zinc.clear_empty().get_dict()

summary = deep_dict()
summary.nzp_concentrate = dict(type="number", min_normal=5, max_normal=20000)
summary.nzp_zn = dict(type="number", min_normal=5, max_normal=20000)
summary.sklad_concentrate = dict(type="number", min_normal=5, max_normal=20000)
summary.sklad_zn = dict(type="number", min_normal=5, max_normal=20000)
summary_table_desc = summary.clear_empty().get_dict()
