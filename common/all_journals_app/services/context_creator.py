from datetime import date, datetime
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

def get_page_mode(request, page):
    page_mode = request.GET.get('page_mode')
    employee = Employee.objects.get(user=request.user)
    plant = request.path.split("/")[1]
    app = 'all_journals_app'
    plant_permission_name = app + ".modify_" + plant
    if not page_mode:
        if employee.user.has_perm(plant_permission_name):
            print(page.shift_is_active, employee.user.has_perm(app + ".edit_cells"), employee.user.has_perm(app + ".validate_cells"))
            if page.shift_is_active and employee.user.has_perm(app + ".edit_cells"):
                return "edit"
            if employee.user.has_perm(app + ".validate_cells"):
                return "validate"
        return "view"
    return page_mode


def get_common_context(journal_name, request, page_type="shift"):
    res = deep_dict()
    res.page_type = page_type

    res.page_id = request.GET.get('id', None)
    plant_name = request.path.split("/")[1]
    plant = Plant.objects.get(name=plant_name)
    # get exact journal page

    if res.page_type == 'shift':
        if res.page_id:
            page = JournalPage.objects.get(id=res.page_id)
        else:
            for shift_order in range(1, plant.number_of_shifts+1):
                page = JournalPage.objects.get_or_create(
                    journal_name=journal_name,
                    shift_date=date.today(),
                    shift_order=shift_order,
                    type=page_type,
                    plant=plant
                )[0]
                if page.shift_is_active:
                    break
        res.shift_is_active = page.shift_is_active
        res.shift_order = page.shift_order
        res.shift_date = page.shift_date
        res.page_mode = get_page_mode(request, page)

    if res.page_type == 'equipment':
        if res.page_id:
            page = JournalPage.objects.get(id=res.page_id)
        else:
            page = JournalPage.objects.get_or_create(
                journal_name=journal_name,
                plant=plant,
                type=res.page_type
            )[0]

    page.save()

    res.full_data = get_full_data(page)
    res.fields_info = get_fields_info()

    res.unfilled_cell = "Unfilled"
    res.unfilled_table = deep_dict()
    res.journal_name = page.journal_name
    res.journal_page = page.id


    return res
