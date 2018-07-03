import datetime
from datetime import date
from pprint import pprint

from django.utils import timezone

from common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from common.all_journals_app.models import CellValue, JournalPage
from common.all_journals_app.fields_descriptions import fields_info
from utils.deep_dict import deep_dict
from login_app.models import Employee


def get_full_data(page):
    res = deep_dict()

    for val in CellValue.objects.filter(journal_page=page):
        if val.index is not None:
            res[val.table_name][val.field_name][val.index] = val.value
            res['id'][val.table_name][val.field_name][val.index] = val.id
            res['responsible'][val.table_name] = val.responsible
        else:
            raise ValueError()

    return res


def get_fields_info():
    return fields_info_desc


def get_page_list(journal_name, request, page_type):
    # Тут надо все даты выдернуть и вот это вот все
    today = timezone.now().date()
    return [today - datetime.timedelta(days=1*i) for i in range(30)]

def get_page_mode(request):
    page_mode = request.GET.get('page_mode')
    employee = Employee.objects.get(user=request.user)
    plant = request.path.split("/")[1]
    if not page_mode:
        if plant == employee.plant:
            roles_with_edit_permission = ["laborant", "master"]
            roles_with_validate_permission = ["admin", "boss"]
            if employee.position in roles_with_edit_permission:
                page_mode = "edit"
            if employee.position in roles_with_validate_permission:
                page_mode = "validate"
        else:
            page_mode = "view"
    return page_mode


def get_common_context(journal_name, request):
    res = deep_dict()

    page_id = request.GET.get('id', None)
    # get exact journal page
    if page_id:
        page = JournalPage.objects.get(id=page_id)
    # get latest journal page
    else:
        page = JournalPage.objects.filter(
            journal_name=journal_name).order_by('-shift_date').first()
        if not page:
            page = JournalPage(journal_name=journal_name)
    page.save()

    res.full_data = get_full_data(page)
    res.fields_info = get_fields_info()

    res.unfilled_cell = "Unfilled"
    res.unfilled_table = deep_dict()
    res.journal_name = page.journal_name
    res.journal_page = page.id

    res.shift_order = page.shift_order
    res.shift_date = page.shift_date
    res.page_mode = get_page_mode(request)
    return res
