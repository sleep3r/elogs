from os import walk
import json

from datetime import date, datetime

from django.db import transaction
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.template import loader, TemplateDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from e_logs.common.all_journals_app.models import Cell, CellGroup, Shift, \
    Equipment, Field, Table, Journal, Plant
from e_logs.core.utils.webutils import process_json_view, logged
from e_logs.core.utils.deep_dict import deep_dict
from e_logs.common.all_journals_app.services.page_modes import get_page_mode, \
    plant_permission, PageModeError, has_edited
from e_logs.core.utils.loggers import stdout_logger
from e_logs.common.messages_app.services import messages
from e_logs.core.models import Setting


class JournalView(LoginRequiredMixin, View):
    """
    Common view for a journal.
    Inherit from this class when creating your own journal view.
    """
    @logged
    def get(self, request, plant_name, journal_name):
        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)
        context = self.get_context(request, plant, journal)
        template = loader.get_template('common.html')
        return HttpResponse(template.render(context, request))

    def get_context(self, request, plant, journal):
        context = deep_dict()
        context.page_type = journal.type

        if journal.type == 'shift':
            page_id = request.GET.get('id', None)
            if page_id:
                shift = Shift.objects.get(id=page_id)
            else:
                number_of_shifts = Shift.get_number_of_shifts(journal)
                # create shifts for today and return current shift
                for shift_order in range(1, number_of_shifts + 1):
                    shift = Shift.objects.get_or_create(
                        journal=journal,
                        order=shift_order,
                        date=date.today()
                    )[0]
                    if shift.is_active:
                        break
            context.shift_is_active_or_no_shifts = shift.is_active
            context.shift_order = shift.order
            context.shift_date = shift.date
            page = shift

        if journal.type == 'equipment':
            equipment = Equipment.objects.get_or_create(
                journal=journal
            )[0]
            page = equipment

        # Adding permissions
        context.page_mode = get_page_mode(request, page)
        print('page_mode='+str(context.page_mode))
        context.has_edited = has_edited(request, page)
        context.has_plant_perm = plant_permission(request)
        context.superuser = request.user.is_superuser
        page.save()

        context.tables_paths = json.loads(
            Setting.objects.get(
                name='tables_list',
                journal=journal
            ).value
        )

        context.journal_cells_data = get_cells_data(page)
        context.journal_fields_descriptions = get_fields_descriptions(request, journal)

        context.unfilled_cell = ""
        context.unfilled_table = deep_dict()
        context.journal_name = page.name
        context.journal_page = page.id
        return context


class ShihtaJournalView(JournalView):
    """ View of report_income_outcome_schieht journal """
    @logged
    def get_context(self, request, journal_name, page_type):
        context = super().get_context(request, journal_name, page_type)

        context.months = {
            'January': 'Январь',
            'February': 'Февраль',
            'March': 'Март',
            'April': 'Апрель',
            'May': 'Май',
            'June': 'Июнь',
            'July': 'Июль',
            'August': 'Август',
            'September': 'Сентябрь',
            'October': 'Октябрь',
            'November': 'Ноябрь',
            'December': 'Декабрь'
        }
        context.plan_or_fact = ['plan', 'fact']
        context.date_year = datetime.now().year
        context.cur_month = list(context.months.keys())[date.today().month-1]
        return context


# TODO: Move to common journal scheme
class MetalsJournalView(JournalView):
    """ View of metals_compute journal """
    @logged
    def get_context(self, request, journal_name, page_type):
        from e_logs.common.all_journals_app.fields_descriptions.fields_info import fields_info_desc
        context = super().get_context(request, journal_name, page_type)

        context.sgok_table.columns = [
            "ЗГОК, ВМТ",
            "Арт-ий, ВМТ",
            "Усть-ТАЛ, ВМТ",
            "Кара<wbr>гайлы, ВМТ",
            "Верх-Бер, ВМТ",
            "Бело<wbr>усовка, ВМТ",
            "Жез<wbr>кент, ВМТ",
            "Ер Тай, ВМТ",
            "Н.Широ<wbr>кинский, ВМТ",
            "Лесо<wbr>сиб, ВМТ",
            "Алтын-Топкан, ВМТ",
            "итого ВМТ",
            "ИТОГО СМТ",
            "выданно огарка, ВМТ",
            "потери, ВМТ",
            "огарка переданно, ВМТ",
            "ЦЕХ, ВМТ",
            "Лента, ВМТ",
            "потеря бункеров ОВЦО, ВМТ",
            "лента итого, ВМТ",
            "откло<wbr>нение"
        ]

        context.sgok_table.fields = fields_info_desc.metals_compute.sgok_table.keys()
        context.gof_table.fields = fields_info_desc.metals_compute.gof_table.keys()
        context.avg_month_table.fields = fields_info_desc.metals_compute.avg_month_table.keys()
        return context


@csrf_exempt
@process_json_view(auth_required=False)
@logged
def change_table(request):
    # tn = request.POST['table_name']
    # jp = request.POST['journal_page']

    # page = JournalPage.objects.get(id=int(jp))

    # employee = request.user.employee
    # page.employee_set.add(employee)

    # Cell.objects.filter(table_name=tn, journal_page=page).delete()

    # for field_name in request.POST:
    #     values = request.POST.getlist(field_name)
    #     with transaction.atomic():
    #         for i, val in enumerate(values):
    #             Cell(journal_page=page, value=val, index=i, field_name=field_name, table_name=tn).save()

    return {"status": 1}


def get_cells_data(page):
    return {
        table.name: {
            cell.field.name: {
                cell.index: {
                    'value': cell.value,
                    'id': cell.id,
                    'comment': cell.comment,
                    'responsible': cell.responsible.name
                }
            }
            for cell in Cell.objects.filter(group=page, field__table=table)
        }
        for table in Table.objects.filter(journal=page.journal)
    }


@csrf_exempt
@logged
def get_fields_descriptions(request, journal):
    return {
        table.name: {
            field.name: Setting.objects.get(
                            name='field_description',
                            field=field
                        ).value
            for field in Field.objects.filter(table=table)
        }
        for table in Table.objects.filter(journal=journal)
    }


@logged
def permission_denied(request, exception, template_name='errors/403.html'):
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)}))


@csrf_exempt
@logged
def save_cell(request):
    cell_info = json.loads(request.body)['cell']
    field_name = cell_info['field_name']
    table_name = cell_info['table_name']
    group_id = cell_info['group_id']
    index = cell_info['index']
    responsible = request.user.employee
    value = json.loads(request.body)['value']

    group = CellGroup.objects.get(id=group_id)
    journal = group.journal
    field = Field.objects.get(
        table=Table.objects.get(
            journal=journal,
            name=table_name
        ),
        name=field_name
    )

    if value == '':
        d_cell = get_or_none(Cell,**cell)
        if d_cell:
            d_cell.delete()
    else:
        Cell.objects.update_or_create(
            group=group,
            field=field,
            index=index,
            defaults={
                "value": value,
                "responsible": responsible
            }
        )

    if journal.type == 'shift':
        shift = Shift.objects.get(id=int(cell_info['group_id']))
        shift.employee_set.add(request.user.employee)

    return JsonResponse({"status": 1})
