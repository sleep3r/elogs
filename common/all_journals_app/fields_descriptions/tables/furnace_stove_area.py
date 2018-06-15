from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict

ut = deep_dict()
ut.ks1 = numeric_default   # № печи
ut.val1 = numeric_default  # значение
ut.ks2 = numeric_default   # № печи
ut.val2 = numeric_default  # значение
ut.ks3 = numeric_default   # № печи
ut.val3 = numeric_default  # значение

udel_table_desc = ut.clear_empty().get_dict()