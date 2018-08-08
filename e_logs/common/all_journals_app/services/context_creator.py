import logging
from datetime import date, timedelta
from pprint import pprint

from django.utils import timezone
from django.core.exceptions import PermissionDenied

from e_logs.common.all_journals_app.models import Cell, Shift, Plant
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.common.login_app.models import Employee
from e_logs.core.utils.loggers import err_logger, default_logger
from e_logs.core.utils.webutils import logged
from .page_modes import get_page_mode, plant_permission, PageModeError, has_edited


def get_full_data(page):
    res = DeepDict()

    for val in Cell.objects.filter(group=page):
        if val.index is not None:
            res[val.table_name][val.field_name][val.index] = val.value
            res['id'][val.table_name][val.field_name][val.index] = val.id
            res['comment'][val.table_name][val.field_name][val.index] = val.comment
            res['responsible'][val.table_name][val.field_name][val.index] = val.responsible
        else:
            raise ValueError()

    return res


def get_fields_info():
    from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
    return fields_info_desc


def get_page_list(name, request, page_type):
    # Тут надо все даты выдернуть и вот это вот все
    today = timezone.now().date()
    return [today - timedelta(days=1*i) for i in range(30)]


@logged
def get_common_context(name, request, page_type="shift"):
    res = DeepDict()

    res.page_type = page_type
    res.page_id = request.GET.get('id', None)
    plant_name = request.path.split("/")[1]
    plant = Plant.objects.get(name=plant_name)
    page = get_page(name, page_type, plant, res)

    # Adding permissions
    res.page_mode = get_page_mode(request, page)
    res.has_edited = has_edited(request, page)
    res.has_plant_perm = plant_permission(request)
    res.superuser = request.user.is_superuser
    page.save()

    res.full_data = get_full_data(page)
    res.fields_info = get_fields_info()

    res.unfilled_cell = ""
    res.unfilled_table = DeepDict()
    res.journal_name = page.name
    res.journal_page = page.id

    return res


@logged
def get_page(name, page_type, plant, res):
    if res.page_id:
        page = Shift.objects.get(id=res.page_id)
    elif page_type == 'shift':
        page = get_shift_page(name, plant, page_type)

        res.shift_is_active_or_no_shifts = page.shift_is_active
        res.shift_order = page.shift_order
        res.shift_date = page.shift_date
    elif page_type == 'equipment' or page_type == 'year':
        page = get_other_page(name, plant, page_type)

        res.shift_is_active_or_no_shifts = True
    else:
        page = None

    return page


def get_other_page(name, plant, page_type):
    err_logger.debug('Getting other page: ' + str((name, plant.name, page_type)))
    page = Shift.objects.get_or_create(
        name=name,
        plant=plant,
        type=page_type
    )[0]
    return page


@logged
def get_shift_page(name, plant, page_type):
    err_logger.debug('Getting shift_paged page: ' + str((name, plant.name, page_type)))
    page = None
    for shift_order in range(1, plant.number_of_shifts + 1):
        page = Shift.objects.get_or_create(
            name=name,
            shift_date=date.today(),
            shift_order=shift_order,
            type=page_type,
            plant=plant
        )[0]
        if page.shift_is_active:
            break
    default_logger.debug('Ended shift_paged page: ' + str((name, plant.name, page_type)))
    return page
