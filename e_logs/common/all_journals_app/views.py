import os
import json
import shutil
import pickle
import environ
import zipfile
from datetime import date, datetime, timedelta

from django.shortcuts import redirect
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
from django.views.decorators.csrf import csrf_exempt

from e_logs.common.all_journals_app.services.context_creator import get_context
from e_logs.common.all_journals_app.models import Cell, Shift, Journal, Plant, Comment, Table, Field
from e_logs.common.messages_app.models import Message

from e_logs.core.utils.deep_dict import DeepDict
from e_logs.core.utils.webutils import process_json_view, logged, has_private_journals, get_or_none
env = environ.Env(DEBUG=(bool, False))
environ.Env.read_env("config/settings/.env")


class Index(LoginRequiredMixin, TemplateView):

    def get(self, request, *args, **kwargs):
        homepage_url = Setting.of(employee=self.request.user.employee)['homepage']
        if homepage_url is None:
            self.template_name = 'furnace-index.html'
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            return redirect(homepage_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context = get_context(self.request, plant=None, journal=None)
        return context


class JournalView(LoginRequiredMixin, View):
    """
    Common view for a journal.
    Inherit from this class when creating your own journal view.
    """

    @logged
    @has_private_journals
    def get(self, request, plant_name: str, journal_name: str):
        plant = Plant.objects.get(name=plant_name)
        journal = Journal.objects.get(plant=plant, name=journal_name)
        context = self.get_context(request, plant, journal)
        template = loader.get_template('common.html')
        return HttpResponse(template.render(context, request))

    @staticmethod
    @logged
    def get_context(request, plant, journal) -> DeepDict:
        return get_context(request, plant, journal)


journal_view = JournalView.as_view()
# journal_view = cached_view_as(Cell)(journal_view)


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
        context.cur_month = list(context.months.keys())[date.today().month - 1]
        return context


# TODO: Move to common journal scheme
class MetalsJournalView(JournalView):
    """ View of metals_compute journal """

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


@logged
def permission_denied(request, exception, template_name='errors/403.html') -> HttpResponse:
    """ View for action with denied permission """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
    return HttpResponseForbidden(
        template.render(request=request, context={'exception': str(exception)}))



@csrf_exempt
@process_json_view(auth_required=False)
# @logged
def save_cell(request):
    if request.is_ajax() and request.method == 'POST':
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
               from_date=timezone.now().date() - timedelta(days=30),  # TODO: make aware
               to_date=timezone.now().date()):
    """Creates shifts for speficied period of time"""

    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    def shift_event(request, shift, is_owned):
        return {
            'title': '{} смена'.format(shift.order),
            'start': shift.start_time,
            'url': '?id={}'.format(shift.id),
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
        for shift_date in date_range(from_date, to_date + timedelta(days=2)):
            for shift_order in range(1, number_of_shifts + 1):
                shift = Shift.get_or_create(journal, shift_order, shift_date)
                is_owned = shift in owned_shifts
                result.append(shift_event(request, shift, is_owned))
        return result
    else:
        raise TypeError('Attempt to get shifts for non-shift journal')


class ConstructorView(LoginRequiredMixin, View):
    def post(self, request):
        pass


class Log():
    def __init__(self, file):
        required_version = env('CONSTRUCTOR_VERSION')

        self.file = zipfile.ZipFile(file)
        meta = None
        try:
            meta = json.loads(self.file.read('meta.json'))
        except ImportError('Ошибка структуры файла'):
            pass

        if meta and meta['version'] == required_version:
            self.name = meta['name']
            self.verbose = meta['verbose']
            self.plant = meta['plant']
            self.type = meta['type']
            self.tables = list(meta['tables'].keys())
            self.tables__meta = meta['tables']
        else:
            raise ImportError(f"Некорректная версия, требуется не ниже v{required_version}")

    def create(self):
        tables_path = settings.BASE_DIR / \
                      f"e_logs/common/all_journals_app/templates/tables/" \
                      f"{self.plant}/{self.name}"

        new_journal = self.__create_journal(tables_path)

        tables_list = []

        for table_name in self.tables:
            new_table = self.__create_table(journal=new_journal, name=table_name)

            tables_list.append(
                f"tables/{self.plant}/{self.name}/{table_name}.html")

            meta = self.tables__meta[table_name]['meta']
            for field_name in meta.keys():
                new_field = self.__create_field(table=new_table,
                                                name=field_name,
                                                meta=meta)

                self.__set_field_settings(field=new_field, meta=meta)

        for table in self.file.namelist():
            if table.startswith('tables/'):
                self.file.extract(table, tables_path)

        Setting.of(new_journal)['tables_list'] = pickle.dumps(tables_list)

    def __create_journal(self, tables_path):
        journal = get_or_none(Journal, name=self.name,
                              plant=Plant.objects.get(name=self.plant),
                              type=self.type)
        if journal:
            raise NameError("Журнал с таким именем уже существует")
        else:
            new_journal = Journal.objects.create(name=self.name,
                                                 verbose_name=self.verbose,
                                                 plant=Plant.objects.get(name=self.name),
                                                 type=self.type)

            if os.path.exists(tables_path):
                raise NameError("Журнал с таким именем уже существует")
            else:
                os.makedirs(tables_path)

                return new_journal

    def __create_table(self, name, journal):
        table = get_or_none(Table, name=name,
                            journal=journal)
        if table:
            raise NameError("Таблица с таким именем уже существует")
        else:
            new_table = Table.objects.create(name=name,
                                    journal=journal,
                                    verbose_name=self.tables__meta[name].get('verbose', None))
            return new_table

    def __create_field(self, table, name, meta):
        field = get_or_none(Field, name=name,
                            table=table)
        if field:
            raise NameError("Столбец с таким именем уже существует")
        else:
            new_field = Field.objects.create(name=name,
                                             table=table,
                                             verbose_name=meta[name].get('verbose', None))
            return new_field

    def __set_field_settings(self, field, meta):
        Setting.of(field)['min_normal'] = meta.get('min_value', None)
        Setting.of(field)['max_normal'] = meta.get('max_value', None)
        Setting.of(field)['units'] = meta.get('units', None)
        Setting.of(field)['type'] = meta.get('type', None)
        if meta['type'] == 'datalist':
            Setting.of(field)['options'] = meta.get('options', None)
