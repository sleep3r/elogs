import json
from datetime import date, timedelta

from django.views.decorators.csrf import csrf_exempt

from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.loggers import default_logger
from e_logs.common.all_journals_app.models import *
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.services.page_modes import get_page_mode, has_edited, \
    plant_permission
# from e_logs.common.all_journals_app.views import JournalView
from e_logs.core.utils.webutils import logged, process_json_view


@logged
def get_context(request, plant, journal) -> DeepDict:
    context = DeepDict()
    context.page_type = journal.type

    if journal.type == 'shift':
        page_id = request.GET.get('id', None)
        page = get_shift(journal, pid=page_id)

        context.shift_is_active_or_no_shifts = page.is_active
        context.shift_order = page.order
        context.shift_date = page.date

    elif journal.type == 'equipment':
        equipment = Equipment.objects.get_or_create(journal=journal)[0]
        page = equipment
    else:
        raise NotImplementedError()

    page.save()

    # Adding permissions
    default_logger.info('page_mode=' + str(context.page_mode))
    context.page_mode = get_page_mode(request, page)
    context.has_edited = has_edited(request, page)
    context.has_plant_perm = plant_permission(request)
    context.superuser = request.user.is_superuser

    context.tables_paths = json.loads(Setting.get_value(name='tables_list', obj=journal))

    context.journal_cells_data = get_cells_data(page)
    context.journal_fields_descriptions = get_fields_descriptions(journal)

    context.journal_name = journal.name
    context.journal_page = page.id
    return context


def get_comments_descriptions(cell):
    return ''.join(map(lambda a: a.text if a else '',
                       Comment.objects.filter(cell=cell)
                       ))


def get_cells_data(page: CellGroup) -> dict:
    def cell_desc(cell):
        return {
            'value': cell.value,
            'id': cell.id,
            'comment': ''.join(map(lambda a: a.text if a else '',
                                   Comment.objects.filter(cell=cell)
                                   )),
            'responsible': cell.responsible.name if cell.responsible else ''
        }

    return {
        table.name: {cell.name: {cell.index: cell_desc(cell)}
                     for cell in table.cells(page)}
        for table in page.tables()
    }


@logged
def get_fields_descriptions(journal: Journal) -> dict:
    def field_descs(table):
        return {field.name: Setting.of(field)['field_description'] for field in table.fields.all()}

    return {table.name: field_descs(table) for table in journal.tables.all()}


@logged
def get_shift(journal, pid=None) -> Shift:
    shift = None

    if pid:
        shift = Shift.objects.get(id=pid)
    else:
        number_of_shifts = Shift.get_number_of_shifts(journal)
        assert number_of_shifts > 0, "<= 0 number of shifts"

        # create shifts for today and return current shift
        for shift_order in range(1, number_of_shifts + 1):
            shift = Shift.objects.get_or_create(journal=journal, order=shift_order,
                                                date=date.today())[0]
            if shift.is_active:
                break

    return shift
