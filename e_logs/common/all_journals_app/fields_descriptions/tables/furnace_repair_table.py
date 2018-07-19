from e_logs.common.all_journals_app.fields_descriptions.fields_classes import *
from e_logs.core.utils.deep_dict import deep_dict


rt = deep_dict()
rt.position_number = number_default  # № позиции по титульному списку СУД
rt.pp = number_default  # № п/п
rt.department = text_default # Подразделение
rt.name_of_object = text_default # Наименование объекта
rt.inv_number = number_default  # № инв
rt.group = numeric_default # Группа значимости
rt.work_center = text_default # рабоч центр
rt.tax_group = number_default  # № налоговой группы
rt.description = text_default # Описание работ
rt.executor = text_default # Исполнитель




repair_table_desc = rt.clear_empty().get_dict()
