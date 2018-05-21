from utils.deep_dict import deep_dict


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