import json
from utils.deep_dict import deep_dict

big_table_desc = deep_dict()

# heareds
big_table_desc.headers.wagon_num.text = 'Номер вагона'
big_table_desc.headers.conc_num.text = 'Наименование концентрата'
big_table_desc.headers.supply_time.text = 'Время поставки'

big_table_desc.headers.dispatch_time.text = 'Время сообщения диспетчеру'
big_table_desc.headers.downtime.text = 'Время перепростоя'
big_table_desc.headers.recieved_conc.text = 'Поступило контейнеров'
big_table_desc.headers.recieved_beds.text = 'Поступило поддонов'
big_table_desc.headers.recieved_stops.text = 'Поступило упоров'
big_table_desc.headers.recieved_braces.text = 'Поступило скоб'


# arrays
big_table_desc.array_fields.wagon_num = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.array_fields.conc_num.text = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.array_fields.supply_time.text = {"type": "number", "min_normal": 10, "max_normal": 100}

big_table_desc.array_fields.dispatch_time.text = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.array_fields.downtime.text = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.array_fields.recieved_conc.text = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.array_fields.recieved_beds.text = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.array_fields.recieved_stops.text = {"type": "number", "min_normal": 10, "max_normal": 100}
big_table_desc.array_fields.recieved_braces.text = {"type": "number", "min_normal": 10, "max_normal": 100}

big_table_desc = big_table_desc.clear_empty().get_dict()

# --------------------------------------- small table -----------------------------------------------------



