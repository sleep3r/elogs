import json
from utils.deep_dict import deep_dict


ut = deep_dict()
#------Upper Table--------
ut.master = dict(type="text", min_normal=10, max_normal=1000)
ut.senior_crane_operator = dict(type="text", min_normal=10, max_normal=1000)

ut.storage = dict(type="text", min_normal=10, max_normal=1000)
ut.crane_operator = dict(type="text", min_normal=10, max_normal=1000)
ut.sling_operator = dict(type="text", min_normal=10, max_normal=1000)

ut.date = dict(type="time", min_normal=10, max_normal=1000)
ut.shift = dict(type="text", min_normal=10, max_normal=1000)

bt = deep_dict()

#-------Big Table-------------
bt.wagon_num = dict(type="number", min_normal=10, max_normal=1000)
bt.conc_num = dict(type="text", min_normal=10, max_normal=1000)

bt.supply_time = dict(type="time", min_normal=10, max_normal=1000)
bt.dispatch_time = dict(type="time", min_normal=10, max_normal=1000)
bt.downtime = dict(type="time", min_normal=10, max_normal=1000)

bt.recieved_conc = dict(type="number", min_normal=10, max_normal=1000, units='шт')
bt.recieved_beds = dict(type="number", min_normal=10, max_normal=1000, units='шт')
bt.recieved_stops = dict(type="number", min_normal=10, max_normal=1000, units='шт')
bt.recieved_braces = dict(type="number", min_normal=10, max_normal=1000, units='шт')


st = deep_dict()
#--------Small Table------------
st.storage = dict(type="number", min_normal=0, max_normal=100)
st.containers_reciept= dict(type="number", min_normal=0, max_normal=100)

st.shipped_empty_num = dict(type="number", min_normal=0, max_normal=100)
st.poured_containers_num = dict(type="number", min_normal=0, max_normal=100)
st.residue_empty_containers1 = dict(type="number", min_normal=0, max_normal=100)
st.residue_empty_containers2 = dict(type="number", min_normal=0, max_normal=100)
st.residue_defective_containers = dict(type="number", min_normal=0, max_normal=100)

st.residue_beds = dict(type="number", min_normal=0, max_normal=100)
st.residue_stops = dict(type="number", min_normal=0, max_normal=100)
st.residue_braces = dict(type="number", min_normal=0, max_normal=100)

st.storage_total = dict(type="number", min_normal=0, max_normal=100)
st.containers_reciept_total = dict(type="number", min_normal=0, max_normal=100)

st.shipped_empty_num_total = dict(type="number", min_normal=0, max_normal=100)
st.poured_containers_num_total = dict(type="number", min_normal=0, max_normal=100)
st.residue_empty_containers1_total = dict(type="number", min_normal=0, max_normal=100)
st.residue_empty_containers2_total = dict(type="number", min_normal=0, max_normal=100)
st.residue_defective_containers_total = dict(type="number", min_normal=0, max_normal=100)

st.residue_beds_total = dict(type="number", min_normal=0, max_normal=100)
st.residue_stops_total = dict(type="number", min_normal=0, max_normal=100)
st.residue_braces_total = dict(type="number", min_normal=0, max_normal=100)

#---------lower table----------
lt = deep_dict()

lt.notes = dict(type="text", min_normal=0, max_normal=100)


big_table_desc = bt.clear_empty().get_dict()
small_table_desc = st.clear_empty().get_dict()
upper_table_desc = ut.clear_empty().get_dict()
lower_table_desc = lt.clear_empty().get_dict()


# --------------------------------------- small table -----------------------------------------------------
