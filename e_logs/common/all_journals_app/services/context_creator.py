import json

from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.loggers import err_logger
from e_logs.common.all_journals_app.models import *
from e_logs.core.models import Setting
from e_logs.common.all_journals_app.services.page_modes import get_page_mode, has_edited, \
    plant_permission
from e_logs.core.utils.webutils import logged, default_if_error


@logged
def get_context(request, page) -> DeepDict:
    context = DeepDict()

    journal = page.journal
    add_type_specific_info(context, journal, page)
    add_permissions(context, page, request)
    add_page_info(context, journal, page)
    context.tables_paths = get_tables_paths(journal)
    context.journal_cells_data = get_cells_data(page)
    context.journal_fields_descriptions = get_fields_descriptions(journal)

    return context


def add_type_specific_info(context, journal, page):
    if journal.type == 'shift':
        context.shift_is_active_or_no_shifts = page.is_active
        context.shift_order = page.order
        context.shift_date = page.date


def add_page_info(context, journal, page):
    context.page_type = journal.type
    context.journal_name = journal.name
    context.journal_page = page.id


def get_tables_paths(journal):
    return Setting.of(journal)['tables_list']


def add_permissions(context, page, request):
    err_logger.info('page_mode=' + str(context.page_mode))
    context.page_mode = get_page_mode(request, page)
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
            'comment': cell.get_comments_text(),
            'responsible': get_responsible_name(cell)
        }

    def table_desc(table):
        cells = table.cells(page)
        err_logger.debug(f'cells: {cells}')
        desc = {cell.name: {c.index: cell_desc(c) for c in cells.filter(field__name=cell.name)} for cell in cells}
        return desc

    desc = {table.name: table_desc(table) for table in page.tables()}

    return desc


@logged
def get_fields_descriptions(journal: Journal) -> dict:
    def field_descs(table):
        return {field.name: Setting.of(obj=field)['field_description']
                for field in table.get_fields()}

    return {table.name: field_descs(table) for table in journal.tables.all()}
