import json
from utils.deep_dict import deep_dict

big_table_desc = deep_dict()

# heareds
big_table_desc.wagon_num_header.text = 'Номер вагона'
big_table_desc.conc_num_header.text = 'Наименование концентрата'
big_table_desc.supply_time_header.text = 'Время поставки'

big_table_desc.dispatch_time_header.text = 'Время сообщения диспетчеру'
big_table_desc.downtime_header.text = 'Время перепростоя'
big_table_desc.recieved_conc_header.text = 'Поступило контейнеров'
big_table_desc.recieved_beds_header.text = 'Поступило поддонов'
big_table_desc.recieved_stops_header.text = 'Поступило упоров'
big_table_desc.recieved_braces_header.text = 'Поступило скоб'


# arrays
big_table_desc.wagon_num = {"type": "number", "min_normal": 10, "max_normal": 100, }
big_table_desc.conc_num = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.supply_time = {"type": "number", "min_normal": 10, "max_normal": 100}

big_table_desc.dispatch_time = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.downtime = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.recieved_conc = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.recieved_beds = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.recieved_stops = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.recieved_braces = {"type": "number", "min_normal": 10, "max_normal": 100}

big_table_desc = big_table_desc.clear_empty().get_dict()

# --------------------------------------- small table -----------------------------------------------------



