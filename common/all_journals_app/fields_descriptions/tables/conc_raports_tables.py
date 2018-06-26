import json
from utils.deep_dict import deep_dict
from common.all_journals_app.fields_descriptions.fields_classes import *


ut = deep_dict()
#------Upper Table--------
ut.master = employee_default
ut.senior_crane_operator = employee_default

ut.storage = dict(type="text", min_normal=10, max_normal=1000, units='№')
ut.crane_operator = employee_default
ut.sling_operator = employee_default

ut.date = dict(type="date", min_normal=10, max_normal=1000)
ut.shift = dict(type="text", min_normal=10, max_normal=1000, units='№')

bt = deep_dict()

#-------Big Table-------------
bt.wagon_num = dict(type="number", min_normal=10, max_normal=1000, units = '№')
bt.conc_num = text_default

bt.supply_time = dict(type="time", min_normal=10, max_normal=1000)
bt.dispatch_time = dict(type="time", min_normal=10, max_normal=1000)
bt.downtime = dict(type="time", min_normal=10, max_normal=1000)

bt.recieved_conc = dict(type="number", min_normal=10, max_normal=1000, units='шт')
bt.recieved_beds = dict(type="number", min_normal=10, max_normal=1000, units='шт')
bt.recieved_stops = dict(type="number", min_normal=10, max_normal=1000, units='шт')
bt.recieved_braces = dict(type="number", min_normal=10, max_normal=1000, units='шт')


st = deep_dict()
#--------Small Table------------

field_names = [
    "storage",
    "containers_reciept",
    "shipped_empty_num",
    "poured_containers_num",
    "residue_empty_containers1",
    "residue_empty_containers2",
    "residue_defective_containers",
    "residue_braces",
    "residue_beds",
    "residue_stops"
]

fields_info = [
    dict(type="text", min_normal=0, max_normal=100),
] + [dict(type="number", min_normal=0, max_normal=100, units="шт")] * 9

for index in range(1, 4):
    if index == 3:
        index = "_total"
    for field_name, field_info in zip(field_names, fields_info):
        st[field_name + str(index)] = field_info


#---------lower table----------
lt = deep_dict()

lt.notes = dict(type="text", min_normal=0, max_normal=100)


big_table_desc = bt.clear_empty().get_dict()
small_table_desc = st.clear_empty().get_dict()
upper_table_desc = ut.clear_empty().get_dict()
lower_table_desc = lt.clear_empty().get_dict()


# --------------------------------------- small table -----------------------------------------------------
