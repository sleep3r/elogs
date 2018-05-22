from utils.deep_dict import deep_dict


#------Upper Table--------
ep = deep_dict()

ut = deep_dict()
ut.master = dict(type="text", min_normal=10, max_normal=1000)
ut.senior_crane_operator = dict(type="text", min_normal=10, max_normal=1000)

ut.storage = dict(type="text", min_normal=10, max_normal=1000)
ut.crane_operator = dict(type="text", min_normal=10, max_normal=1000)
ut.sling_operator = dict(type="text", min_normal=10, max_normal=1000)

ut.date = dict(type="time", min_normal=10, max_normal=1000)
ut.shift = dict(type="text", min_normal=10, max_normal=1000)

bt = deep_dict()


#------Loading Schieht Table--------



main_table  = deep_dict()
main_table.concentrate = dict(type="number", min_normal=10, max_normal=1000, units='шт')
main_table.zn = dict(type="number", min_normal=10, max_normal=1000, units='')
main_table.ratio = dict(type="number", min_normal=10, max_normal=1000, units='')

main_table_desc = main_table.clear_empty().get_dict()