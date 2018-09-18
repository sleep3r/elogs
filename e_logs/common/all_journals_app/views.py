import os
import json
import pytz
import shutil
import environ
import zipfile
from datetime import date, datetime, timedelta

from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic import TemplateView, View
from django.conf import settings

from e_logs.core.models import Setting
from e_logs.core.utils.loggers import stdout_logger

from cacheops import cached_as, cached_view_as
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, HttpRequest
from django.template import loader, TemplateDoesNotExist
from django.views import View
from django.shortcuts import redirect, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.urls import reverse

from e_logs.common.all_journals_app.services.context_creator import get_context, Equipment
from e_logs.common.all_journals_app.models import Cell, Shift, Journal, Plant, Comment, Table, Field
from e_logs.common.messages_app.models import Message

from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.webutils import process_json_view, logged, has_private_journals, get_or_none
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env("config/settings/.env")


class Index(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return redirect('/furnace/metals_compute')



class JournalView(LoginRequiredMixin, View):
    """
    Common view for a journal.
    Inherit from this class when creating your own journal view.
    """

    # @has_private_journals
    def get(self, request, plant_name: str, journal_name: str, page_id=None):

        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)
        page = None
        if journal.type == 'shift':
            if page_id:
                page = Shift.objects.get(id=page_id)
            else:
                number_of_shifts = Shift.get_number_of_shifts(journal)
                assert number_of_shifts > 0, "<= 0 number of shifts"

                # create shifts for today and return current shift
                for shift_order in range(1, number_of_shifts + 1):
                    shift = Shift.objects.get_or_create(journal=journal,
                                                        order=shift_order,
                                                        date=timezone.now().date())[0]
                    if shift.is_active:
                        page = shift
                        break
                if not page: # fixme: there may be no active shift due to datetime problems
                    page = shift
                return redirect('journal_view', page_id=page.id, plant_name=plant_name,
                                journal_name=journal_name)
        elif journal.type == 'equipment':
            page = Equipment.objects.get_or_create(journal=journal)[0]
        else:
            raise NotImplementedError()
        context = self.get_context(request, page)
        template = loader.get_template('common.html')
        return HttpResponse(template.render(context, request))

    @staticmethod
    @logged
    def get_context(request, page) -> DeepDict:
        return get_context(request, page)


journal_view = JournalView.as_view()
# journal_view = cached_view_as(Cell)(journal_view)


class ShihtaJournalView(JournalView):
    """ View of report_income_outcome_schieht journal """

    def get(self, request, plant_name='furnace', journal_name='report_income_outcome_schieht'):
        response = super().get(request, plant_name, journal_name)
        return response

    @logged
    def get_context(self, request, page):
        context = super().get_context(request, page)

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
        context.cur_month = list(context.months.keys())[date.today().month - 1]
        return context


# TODO: Move to common journal scheme
class MetalsJournalView(JournalView):
    """ View of metals_compute journal """

    def get(self, request, plant_name='furnace', journal_name='metals_compute'):
        return super().get(request, plant_name, journal_name)

    @logged
    def get_context(self, request, journal_name, page_type) -> DeepDict:
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
def end_shift(request):
    if request.method == 'POST':
        shift_id = request.POST.get('id', None)
        if shift_id:
            shift = Shift.objects.get(id=int(shift_id))
            shift.ended = True
            shift.save()
            return JsonResponse({"status":1})

@logged
def permission_denied(request, exception, template_name='errors/403.html') -> HttpResponse:
    """ View for action with denied permission """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)}))


def get_table_template(request, plant_name, journal_name, table_name):
    return render_to_response(f'tables/{plant_name}/{journal_name}/{table_name}.html')


@csrf_exempt
@process_json_view(auth_required=False)
# @logged
def save_cell(request):
    if request.method == 'POST':
        cell_info = json.loads(request.body)
        cell = Cell.get_or_create_cell(**cell_info['cell_location'])
        value = cell_info['value']
        if value != '':
            cell.responsible = request.user.employee
            cell.value = value
            cell.save()
        else:
            cell.delete()

        if cell.journal.type == 'shift':
            shift = Shift.objects.get(id=int(cell_info['cell_location']['group_id']))
            shift.employee_set.add(request.user.employee)

        return {"status": 1}


@cached_as(Plant, Journal, Shift)
@process_json_view(auth_required=False)
@logged
def get_shifts(request, plant_name: str, journal_name: str,
               from_date=timezone.now().date() - timedelta(days=30),
               to_date=timezone.now().date()):
    """Creates shifts for speficied period of time"""

    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def shift_event(request, shift, is_owned):
        return {
            'title': '{} смена'.format(shift.order),
            'start': shift.start_time,
            'url': '/{}/{}/{}/'.format(shift.journal.plant.name, shift.journal.name, shift.id),
            'title:': 'Some title',
            'color': '#169F85' if is_owned else '#2A3F54'
        }

    result = []
    plant = Plant.objects.get(name=plant_name)
    journal = Journal.objects.get(plant=plant, name=journal_name)
    employee = request.user.employee
    owned_shifts = employee.owned_shifts.all()

    if journal.type == 'shift':
        number_of_shifts = Shift.get_number_of_shifts(journal)

        for shift_date in date_range(from_date, to_date + timedelta(days=1)):
            for shift_order in range(1, number_of_shifts + 1):
                shift = Shift.get_or_create(journal, shift_order, shift_date)
                is_owned = shift in owned_shifts
                result.append(shift_event(request, shift, is_owned))

        return result
    else:
        raise TypeError('Attempt to get shifts for non-shift journal')


class ConstructorView(LoginRequiredMixin, View):
    def post(self, request):
        if request.FILES.get('journal_file', None):
            journal = request.FILES['journal_file']
            plant_name = self.request.POST.get('plant', None)
            type = self.request.POST.get('type', None)
            if plant_name and type:
                plant = Plant.objects.get(name=plant_name)
                try:
                    log = JournalBuilder(request=self.request, file=journal, plant=plant, type=type)
                except FileNotFoundError as err:
                    return render(self.request, 'settings.html',
                                  {'form_errors': str(err)})
                except ImportError as err:
                    return render(self.request, 'settings.html',
                                  {'form_errors': str(err)})
                log.create()

                return redirect('/common/settings/')
            else:
                return render(self.request, 'settings.html', {'form_errors':'Выберите цех и тип!'})

        return render(self.request, 'settings.html', {'form_errors': 'Выберите файл журнала!'})


class JournalBuilder():
    def __init__(self, request, file, plant, type):
        required_version = env('CONSTRUCTOR_VERSION')

        self.request = request
        self.file = zipfile.ZipFile(file)

        try:
            meta = json.loads(self.file.read(f'{file.name.split(".")[0]}/meta.json'))
        except:
            raise FileNotFoundError('Ошибка структуры файла')

        if meta['version'] == float(required_version):
            self.plant = plant
            self.type = type
            self.name = meta['name']
            self.title = meta['title']
            self.tables = meta['tables']
        else:
            raise ImportError(f"Некорректная версия, требуется не ниже v{required_version}")

    def create(self):
        tables_path = settings.BASE_DIR / \
                    f"e_logs/common/all_journals_app/templates/tables/{self.plant.name}/{self.name}"

        new_journal = self.__create_journal(tables_path)

        for table in self.tables:
            new_table = self.__create_table(journal=new_journal, table=table)

            for field in table['fields']:
                new_field = self.__create_field(table=new_table, field=field)
                self.__set_field_settings(field=new_field, meta=field)

        self.__extract_tables(tables_path)

        self.__set_tables_order(journal=new_journal)

    def __create_journal(self, tables_path):
        journal = get_or_none(Journal, name=self.name, plant=self.plant, type=self.type)

        if journal or os.path.exists(tables_path):
            return render(self.request, 'settings.html',
                          {'form_errors': 'Журнал с таким именем уже существует!'})
        else:
            new_journal = Journal.objects.create(name=self.name,
                                                 verbose_name=self.title,
                                                 plant=self.plant,
                                                 type=self.type)
            # os.makedirs(tables_path)

            return new_journal

    def __create_table(self, journal, table):
        table = get_or_none(Table, name=table['name'], journal=journal)

        if table:
            journal.delete()
            return render(self.request, 'settings.html',
                          {'form_errors': f'Две таблицы с одинаковым именем {table["name"]}!'})
        else:
            new_table = Table.objects.create(name=table['name'],
                                        journal=journal,
                                        verbose_name=table.get('title', None))
            return new_table

    def __create_field(self, table, field):
        field = get_or_none(Field, name=field['name'], table=table)

        if field:
            table.journal.delete()
            return render(self.request, 'settings.html',
                          {'form_errors': f'Две столбца с одинаковым именем {field["name"]}!'})
        else:
            new_field = Field.objects.create(name=field.pop('name'),
                                             table=table,
                                             verbose_name=field.get('title', None))
            return new_field

    def __set_field_settings(self, field, meta):
        Setting.of(field)["field_description"] = meta

    def __extract_tables(self, tables_path):
        for table in self.file.infolist():
            if table.filename.endswith('.html'):
                table.filename = os.path.basename(table.filename)
                self.file.extract(table, tables_path)

    def __set_tables_order(self, journal):
        tables_list = []
        for table in sorted(self.tables, key=lambda t:t['order']):
            tables_list.append(f"tables/{self.plant.name}/{self.name}/{table.name}.html")
        Setting.of(journal)['tables_list'] = tables_list