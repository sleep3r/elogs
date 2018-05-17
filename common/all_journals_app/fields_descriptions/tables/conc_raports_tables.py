import json
from utils.deep_dict import deep_dict

tt = deep_dict()

# arrays
tt.wagon_num = dict(type="number", min_normal=0, max_normal=100)
tt.conc_num = dict(type="text", min_normal=0, max_normal=100)

tt.supply_time = dict(type="time", min_normal=0, max_normal=100)
tt.dispatch_time = dict(type="time", min_normal=0, max_normal=100)
tt.downtime = dict(type="time", min_normal=0, max_normal=100)

tt.recieved_conc = dict(type="number", min_normal=5, max_normal=100)
tt.recieved_beds = dict(type="number", min_normal=0, max_normal=100)
tt.recieved_stops = dict(type="number", min_normal=0, max_normal=100)
tt.recieved_braces = dict(type="number", min_normal=0, max_normal=100)

big_table_desc = tt.clear_empty().get_dict()

# --------------------------------------- small table -----------------------------------------------------



