import json
from utils.deep_dict import deep_dict

big_table_desc = deep_dict()

# arrays
big_table_desc.wagon_num = dict(type="number", min_normal=0, max_normal=100)
big_table_desc.conc_num = dict(type="text", min_normal=0, max_normal=100)

big_table_desc.supply_time = dict(type="time", min_normal=0, max_normal=100)
big_table_desc.dispatch_time = dict(type="time", min_normal=0, max_normal=100)
big_table_desc.downtime = dict(type="time", min_normal=0, max_normal=100)

big_table_desc.recieved_conc = dict(type="number", min_normal=5, max_normal=100)
big_table_desc.recieved_beds = dict(type="number", min_normal=0, max_normal=100)
big_table_desc.recieved_stops = dict(type="number", min_normal=0, max_normal=100)
big_table_desc.recieved_braces = dict(type="number", min_normal=0, max_normal=100)

big_table_desc = big_table_desc.clear_empty().get_dict()

# --------------------------------------- small table -----------------------------------------------------



