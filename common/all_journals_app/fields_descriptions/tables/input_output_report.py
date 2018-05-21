from utils.deep_dict import deep_dict


#------Upper Table--------
ep = deep_dict()
ut.master = dict(type="text", min_normal=10, max_normal=1000)
ut.senior_crane_operator = dict(type="text", min_normal=10, max_normal=1000)

ut.storage = dict(type="text", min_normal=10, max_normal=1000)
ut.crane_operator = dict(type="text", min_normal=10, max_normal=1000)
ut.sling_operator = dict(type="text", min_normal=10, max_normal=1000)

ut.date = dict(type="time", min_normal=10, max_normal=1000)
ut.shift = dict(type="text", min_normal=10, max_normal=1000)

bt = deep_dict()