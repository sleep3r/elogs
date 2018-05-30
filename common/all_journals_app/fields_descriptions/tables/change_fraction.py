from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict


cft = deep_dict()
cft.date_start = date_default
cft.shift_number = numeric_default
cft.massa_fur = numeric_default
cft.massa_sit = numeric_default
cft.fraction = numeric_default
cft.executer = text_default

change_fraction_table_desc = cft.clear_empty().get_dict()