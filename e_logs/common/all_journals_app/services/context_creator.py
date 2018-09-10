import json

from e_logs.business_logic.modes.models import FieldConstraints, Mode
from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.loggers import err_logger
from e_logs.common.all_journals_app.models import *
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.services.page_modes import get_page_mode, has_edited, \
    plant_permission
from e_logs.core.utils.webutils import logged, default_if_error, get_or_none


@logged
def get_context(request, plant, journal) -> DeepDict:
    context = DeepDict()

    page = get_page(journal, request)

    add_type_specific_info(context, journal, page)
    add_permissions(context, page, request)
    add_page_info(context, journal, page)
    context.tables_paths = get_tables_paths(journal)
    context.journal_cells_data = get_cells_data(page)
    context.journal_fields_descriptions = get_fields_descriptions(journal)
    context.plant = plant

    return context


def add_type_specific_info(context, journal, page):
    if journal.type == 'shift':
        context.shift_is_active_or_no_shifts = page.is_active
        context.shift_order = page.order
        context.shift_date = page.date


def get_page(journal, request):
    if journal.type == 'shift':
        page_id = request.GET.get('id', None)
        page = Shift.get_shift(journal, pid=page_id)
    elif journal.type == 'equipment':
        equipment = Equipment.objects.get_or_create(journal=journal)[0]
        page = equipment
    else:
        raise NotImplementedError()
    return page


def add_page_info(context, journal, page):
    context.page_type = journal.type
    context.journal_name = journal.name
    context.journal_page = page.id
    context.page_is_closed = page.closed


def get_tables_paths(journal):
    return Setting.of(journal)['tables_list']


def add_permissions(context, page, request):
    # err_logger.info('page_mode=' + str(context.page_mode))
    context.page_mode = get_page_mode(request, page)
    context.employee_list = page.employee_set.all()
    context.has_edited = has_edited(request, page)
    context.has_plant_perm = plant_permission(request)
    context.superuser = request.user.is_superuser

@default_if_error(value='')
def get_responsible_name(cell: Cell):
    return cell.responsible.name


def get_cells_data(page: CellGroup) -> dict:
    def cell_desc(cell):
        return {
            'value': cell.value,
            'id': cell.id,
            'comment': cell.get_comments_text(cell),
            'responsible': get_responsible_name(cell)
        }

    def table_desc(table):
        cells = table.cells(page)
        desc = {cell.name: {c.index: cell_desc(c) for c in cells.filter(field__name=cell.name)} for cell in cells}
        return desc

    desc = {table.name: table_desc(table) for table in page.tables()}

    return desc


@logged
def get_fields_descriptions(journal: Journal) -> dict:
    def get_field_desc(journal, field):
        constraint = Mode.get_active_constraint(field=field, journal=journal)
        desc = Setting.of(obj=field)['field_description']

        if constraint:
            desc['min_normal'] = constraint.min_normal
            desc['max_normal'] = constraint.max_normal

        return desc

    def field_descs(journal, table):
        return {field.name: get_field_desc(journal, field)
                for field in table.get_fields()}

    return {table.name: field_descs(journal, table) for table in journal.tables.all()}
