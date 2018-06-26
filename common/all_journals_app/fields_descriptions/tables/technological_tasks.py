from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict



ts = deep_dict()
ts.date_create = date_default
ts.comments = text_default
ts.caption = dict(type="datalist", min_normal=10, max_normal=20000, options=["ЗГОК", "Арт-ий",
                                                                             "Усть-ТАЛ",
                                                                             "Карагайлы",
                                                                             "Верх-Бер",
                                                                             "Белоусовка",
                                                                             "Жезкент",
                                                                             "Н.Широкинский",
                                                                             "Лесосиб",
                                                                             "Алтын-Топкан"])

ts.weight = ton_default

ts.employee = employee_default

technologial_tasks_main_desc = ts.clear_empty().get_dict()
