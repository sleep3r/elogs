from common.all_journals_app.fields_descriptions.fields_classes import *
from utils.deep_dict import deep_dict


rt = deep_dict()
rt.position_number = numeric_default # № позиции по титульному списку СУД
rt.pp = numeric_default # № п/п
rt.department = text_default # Подразделение
rt.name_of_object = text_default # Наименование объекта
rt.inv_number = numeric_default # № инв
rt.group = numeric_default # Группа значимости
rt.work_center = text_default # рабоч центр
rt.tax_group = text_default # № налоговой группы
rt.description = text_default # Описание работ
rt.executor = text_default # Исполнитель




repair_table_desc = rt.clear_empty().get_dict()