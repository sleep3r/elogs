from common.all_journals_app.fields_descriptions.fields_classes import date_default, text_default
from utils.deep_dict import deep_dict

lt = deep_dict()

lt.time1 = text_default
lt.time2 = text_default
lt.time3 = text_default
lt.time4 = text_default
lt.defence1 = text_default
lt.defence2 = text_default
lt.defence3 = text_default
lt.defence4 = text_default
lt.weight1 = text_default
lt.passed_fio = text_default
lt.accepted_fio = text_default
lt.sign1 = text_default
lt.sign2 = text_default
lt.sign3 = text_default
lt.sign4 = text_default
lt.weight2 = text_default
lt.passed_sing = text_default
lt.accepted_sign = text_default


last_table_desc = lt.clear_empty().get_dict()