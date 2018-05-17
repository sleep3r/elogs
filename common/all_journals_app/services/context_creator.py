from pprint import pprint

from common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from common.all_journals_app.models import CellValue, JournalPage
from common.all_journals_app.fields_descriptions import fields_info
from utils.deep_dict import deep_dict


def get_full_data(page):
    res = deep_dict()

    for val in CellValue.objects.filter(journal_page=page):
        if val.index is not None:
            res[val.table_name][val.field_name][val.index] = val.value
        else:
            res[val.table_name][val.field_name] = val.value

    return res


def get_fields_info():
    return fields_info_desc


def get_common_context(page):
    res = deep_dict()

    res['full_data'] = get_full_data(page)
    res['fields_info'] = get_fields_info()

    res.journal_name = page.journal_name
    res.journal_page = page.id

    return res
