from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict


fs = deep_dict()
fields_p = ["pb", "cu", "cd","fe", "SiO2", "Zn_furn", "Pb2", "Pb3", "Pb4", "Pb5"]

for field_name in fields_p:
    fs[field_name] = percent_default

fs['vmt'] = vmt_default
fs['cmt'] = smt_default
fs['zn_end'] = ton_default

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

sns['cmt'] = smt_default


sns_fields_p = ["znp","Pb_", "Cu_", "Cd_"]
for field_name in sns_fields_p:
    sns[field_name] = percent_default

sns_fields_m = ["SodZn", "SodPb", "SodCu", "SodCd", "Au", "Ag"]
for field_name in sns_fields_m:
    sns[field_name] = ton_default

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

zgok_fields = ["zgok", "art-iy", "ust-tal", "karagayls", "verh-ber", "belousovka", "Jezkent",
               "er-tay", "NShirokinskiy", "lesosib", "altyn-topkan", "itogo_vmt", "itogo_smt", "vydano_ogarka", "poteri",
               "ogarka_peredano", "ceh", "Lenta", "poterya", "lenta_itogo"]


for field_name in zgok_fields:
    zgok[field_name] = vmt_default

zgok['deviation'] = text_default
sgok_table_desc = zgok.clear_empty().get_dict()


gof = deep_dict()
gof_fields_smt = ["cmt", "cmt2", "cmt3", "cmt4", "cmt5", "cmt6", "cmt7", "cmt8"]
gof_fields_ton = ["zinc", "zinc2", "zinc3", "zinc4", "zinc5", "zinc6", "zinc7", "zinc8"]

gof['vmt'] = vmt_default

for smt,zink in zip(gof_fields_smt, gof_fields_ton):
    gof[smt] = smt_default
    gof[zink] = ton_default
# for field_name in gof_fields_ton:
#     gof[field_name] = ton_default


gof_table_desc = gof.clear_empty().get_dict()


