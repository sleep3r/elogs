import datetime
from datetime import date
from pprint import pprint

from django.utils import timezone

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
            raise ValueError()

    return res


def get_fields_info():
    return fields_info_desc


def get_page_list(journal_name, request, page_type):
    # Тут надо все даты выдернуть и вот это вот все
    today = timezone.now().date()
    return [today - datetime.timedelta(days=1*i) for i in range(30)]


def get_common_context(journal_name, request, page_type="shift"):
    res = deep_dict()

    page = JournalPage.objects.get_or_create(
        journal_name=journal_name,
        type=page_type)[0]
    page.save()

    res['full_data'] = get_full_data(page)
    res['fields_info'] = get_fields_info()

    res.unfilled_cell = "Unfilled"
    res.unfilled_table = deep_dict()
    res.journal_name = page.journal_name
    res.journal_page = page.id

    page_mode = request.GET.get('page_mode') or 'edit'

    print(page_mode)

    if page_mode == 'view':
        res.editable = 'readonly'
    elif page_mode == 'edit':
        res.editable = ''
    elif page_mode == 'validate':
        res.editable = 'readonly'
        res.validate = True

    return res
