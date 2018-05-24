from common.all_journals_app.fields_descriptions.fields_classes import numeric_default
from utils.deep_dict import deep_dict


fs = deep_dict()
fields = ["vmt","cmt", "zn_end", "pb", "cu", "cd_fe", "SiO2", "Zn_furn", "Pb2", "Pb3", "Pb4", "Pb5"]

for field_name in fields:
    fs[field_name] = dict(type="number", min_normal=10, max_normal=20000)

metals_main_desc = fs.clear_empty().get_dict()

sns = deep_dict()
sns.caption = dict(type="datalist", min_normal=10, max_normal=20000, options=["ЗГОК","Арт-ий",
    "Усть-ТАЛ",
    "Карагайлы",
    "Верх-Бер",
    "Белоусовка",
    "Жезкент",
    "Н.Широкинский",
    "Лесосиб",
    "Алтын-Топкан"])

sns_fields = ["cmt", "znp", "SodZn", "Pb_", "SodPb", "Cu_", "SodCu", "Cd_", "SodCd", "Au", "Ag"]

for field_name in sns_fields:
    sns[field_name] = numeric_default
sns_table_desc = sns.clear_empty().get_dict()


zgok = deep_dict()

zgok_columns = [
"ЗГОК",
"Арт-ий",
"Усть-ТАЛ",
"Карагайлы",
"Верх-Бер",
"Белоусовка",
"Жезкент",
"Ер Тай",
"Н.Широкинский",
"Лесосиб",
"Алтын-Топкан",
"итого ВМТ",
"ИТОГО СМТ",
"выданно огарка",
"потери",
"огарка переданно",
"ЦЕХ",
"Лента",
"потеря бункеров ОВЦО",
"лента итого",
"отклонение"]

zgok_fields = ["sgok", "art-iy", "ust-tal", "karagayls", "verh-ber", "belousovka", "Jezkent",
               "er-tay", "NShirokinskiy", "lesosib", "altyn-topkan", "itogo_vmt", "itogo_smt", "vydano_ogarka", "poteri",
               "ogarka_peredano", "ceh", "Lenta", "poterya", "lenta_itogo", "deviation"
               ]

for field_name in zgok_fields:
    zgok[field_name] = numeric_default

sgok_table_desc = zgok.clear_empty().get_dict()