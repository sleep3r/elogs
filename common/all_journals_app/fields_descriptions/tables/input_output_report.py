from utils.deep_dict import deep_dict


#------Upper Table--------
ep = deep_dict()
ut = deep_dict()
ut.master = dict(type="text", min_normal=10, max_normal=1000)
ut.senior_crane_operator = dict(type="text", min_normal=10, max_normal=1000)
#------year plan schieht--------
eps = deep_dict()
eps.concentrate = dict(type='number', min_normal=10, max_normal=1000)
eps.year_plans = dict(type='number', min_normal=10, max_normal=1000)
eps.month_smt = dict(type='number', min_normal=10, max_normal=1000)
eps.day_smt = dict(type='number', min_normal=10, max_normal=1000)
eps.tonns_a_year = dict(type='number', min_normal=10, max_normal=1000)
eps.schieht_frac = dict(type='number', min_normal=10, max_normal=1000)
eps.zn = dict(type='number', min_normal=10, max_normal=1000)
eps.s = dict(type='number', min_normal=10, max_normal=1000)
eps.h2o = dict(type='number', min_normal=10, max_normal=1000)
eps.fe = dict(type='number', min_normal=10, max_normal=1000)
eps.cu = dict(type='number', min_normal=10, max_normal=1000)
eps.pb = dict(type='number', min_normal=10, max_normal=1000)
eps.sio2 = dict(type='number', min_normal=10, max_normal=1000)
eps.cd = dict(type='number', min_normal=10, max_normal=1000)
eps.cao = dict(type='number', min_normal=10, max_normal=1000)
eps.mgo = dict(type='number', min_normal=10, max_normal=1000)
eps.K = dict(type='number', min_normal=10, max_normal=1000)
eps.na = dict(type='number', min_normal=10, max_normal=1000)
eps.arsenic = dict(type='number', min_normal=10, max_normal=1000)
eps.co = dict(type='number', min_normal=10, max_normal=1000)
eps.au = dict(type='number', min_normal=10, max_normal=1000)
eps.ag = dict(type='number', min_normal=10, max_normal=1000)
eps.vmt = dict(type='number', min_normal=10, max_normal=1000)
eps.norm = dict(type='number', min_normal=10, max_normal=1000)

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