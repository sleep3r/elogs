from utils.deep_dict import deep_dict



#------year plan schieht--------
yps = deep_dict()
yps.concentrate = dict(type='number', min_normal=10, max_normal=1000)
yps.year_plans = dict(type='number', min_normal=10, max_normal=1000)
yps.month_smt = dict(type='number', min_normal=10, max_normal=1000)
yps.day_smt = dict(type='number', min_normal=10, max_normal=1000)
yps.tonns_a_year = dict(type='number', min_normal=10, max_normal=1000)
yps.schieht_frac = dict(type='number', min_normal=10, max_normal=1000)
yps.zn = dict(type='number', min_normal=10, max_normal=1000)
yps.s = dict(type='number', min_normal=10, max_normal=1000)
yps.h2o = dict(type='number', min_normal=10, max_normal=1000)
yps.fe = dict(type='number', min_normal=10, max_normal=1000)
yps.cu = dict(type='number', min_normal=10, max_normal=1000)
yps.pb = dict(type='number', min_normal=10, max_normal=1000)
yps.sio2 = dict(type='number', min_normal=10, max_normal=1000)
yps.cd = dict(type='number', min_normal=10, max_normal=1000)
yps.cao = dict(type='number', min_normal=10, max_normal=1000)
yps.mgo = dict(type='number', min_normal=10, max_normal=1000)
yps.K = dict(type='number', min_normal=10, max_normal=1000)
yps.na = dict(type='number', min_normal=10, max_normal=1000)
yps.arsenic = dict(type='number', min_normal=10, max_normal=1000)
yps.co = dict(type='number', min_normal=10, max_normal=1000)
yps.au = dict(type='number', min_normal=10, max_normal=1000)
yps.ag = dict(type='number', min_normal=10, max_normal=1000)
yps.vmt = dict(type='number', min_normal=10, max_normal=1000)
yps.norm = dict(type='number', min_normal=10, max_normal=1000)
year_plan_schieht_desc = yps.clear_empty().get_dict()

bt = deep_dict()

#------Loading Schieht Table--------

main_table  = deep_dict()
main_table.concentrate = dict(type="number", min_normal=10, max_normal=1000)
main_table.zn = dict(type="number", min_normal=10, max_normal=1000, units='')
main_table.ratio = dict(type="number", min_normal=10, max_normal=1000, units='')
main_table_desc = main_table.clear_empty().get_dict()

#-----Supply of zinc concentrates table ----
supply_zinc = deep_dict()
supply_zinc.concentrate = dict(type="number", min_normal=10, max_normal=20000)
supply_zinc.zn = dict(type="number", min_normal=10, max_normal=10000)
supply_zinc_desc = supply_zinc.clear_empty().get_dict()