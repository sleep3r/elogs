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

sns.zn = dict(type="number", min_normal=10, max_normal=20000)
for field_name in sns_fields:
    sns[field_name] = dict(type="number", min_normal=10, max_normal=20000)
sns_table_desc = sns.clear_empty().get_dict()