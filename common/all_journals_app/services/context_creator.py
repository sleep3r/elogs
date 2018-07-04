import datetime
from datetime import date
from pprint import pprint

from django.utils import timezone

from common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
from common.all_journals_app.models import CellValue, JournalPage, Plant
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
    app = 'all_journals_app'
    plant_permission_name = app + ".modify_" + plant
    if not page_mode:
        if employee.user.has_perm(plant_permission_name):
            if employee.user.has_perm(app + ".edit_cells"):
                return "edit"
            if employee.user.has_perm(app + ".validate_cells"):
                return "validate"
        else:
            return "view"
    return page_mode


def get_common_context(journal_name, request, page_type="shift"):
    res = deep_dict()

    page_id = request.GET.get('id', None)
    plant = request.path.split("/")[1]
    # get exact journal page
    if page_id:
        page = JournalPage.objects.get(id=page_id)
    # get latest journal page
    else:
        page = JournalPage.objects.filter(
            journal_name=journal_name).order_by('-shift_date').first()
        if not page:
            page = JournalPage(
                journal_name=journal_name,
                shift_date=date.today(),
                shift_order=1,
                type=page_type,
                plant=Plant.objects.get(name=plant)
            )
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
