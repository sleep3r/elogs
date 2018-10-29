import json
import os
import pickle
import hashlib
from datetime import timedelta
from shutil import copyfile
from urllib.parse import parse_qs

from django.contrib.contenttypes.models import ContentType
from django.core.files.storage import FileSystemStorage
from django.db.models import Prefetch
from django.forms import model_to_dict
from django.views import View
from django.http import JsonResponse
from django.conf import settings

from e_logs.business_logic import services
from e_logs.business_logic.modes.models import Mode, FieldConstraints
from e_logs.common.all_journals_app.models import Plant, Journal, Table, Field, Shift, Cell, Comment
from e_logs.common.all_journals_app.models import CellGroup
from e_logs.common.all_journals_app.services.journal_builder import JournalBuilder
from e_logs.common.all_journals_app.views import get_current_shift
from e_logs.common.all_journals_app.services.page_modes import get_page_mode
from e_logs.common.login_app.models import Employee
from e_logs.core.models import Setting
from e_logs.core.utils.webutils import current_date, date_range
from e_logs.core.views import LoginRequired
from e_logs.core.management.commands.compress_journals import compress_journal


class ShiftAPI(LoginRequired, View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not kwargs.get('id', None):
            journal_name = parse_qs(request.GET.urlencode())['journalName'][0]
            current_shift = get_current_shift(Journal.objects.get(name=journal_name))
            print(current_shift)
            if current_shift:
                id = current_shift.id
            else:
                id = Shift.objects.latest('date').id
        else:
            id = kwargs['id']
        print("shift id", id)
        qs = Shift.objects \
            .select_related('journal', 'journal__plant') \
            .prefetch_related('journal__tables',
                              'journal__tables__fields',
                              Prefetch('group_cells',
                                       queryset=Cell.objects.select_related('field',
                                                                            'field__table',
                                                                            'responsible__user',
                                                                            'responsible').
                                       filter(group_id=id).prefetch_related(
                                           Prefetch('comments', queryset=Comment.objects.all().
                                                    select_related('employee__user',
                                                                   'employee'))))).get(id=id)


        plant = qs.journal.plant
        res = {
            "id": qs.id,
            "plant": {"name": plant.name},
            "order": qs.order,
            "date": qs.date.isoformat(),
            'start_time': qs.start_time.isoformat(),
            "closed": qs.closed,
            "mode": get_page_mode(user=user, plant=plant),
            "responsibles": [{str(e.user): str(e)} for e in qs.responsibles.all()],
            "permissions": self.get_permissions(request, qs),
            "journal": self.journal_serializer(qs)}

        self.add_constraints(qs, res)

        return JsonResponse(res, safe=False)

    def add_constraints(self, qs, res):
        modes = Mode.objects.filter(is_active=True, journal=qs.journal).order_by('beginning')
        if modes.exists():
            mode = modes.last()
            constraints = FieldConstraints.objects.filter(mode=mode)

            for constraint in constraints:
                field = constraint.field
                desc = res['journal']['tables'][field.table.name]['fields'][field.name][
                    'field_description']
                desc['min_normal'] = constraint.min_normal
                desc['max_normal'] = constraint.max_normal


    def get_permissions(self, request, shift):
        def get_time(shift):
            if request.user.has_perm(EDIT_CELLS):
                assignment_time = shift.end_time - timedelta(
                    **Setting.of(shift)['shift_assignment_time'])
                assignment_time = assignment_time.isoformat()
                not_assignment_time = shift.end_time + timedelta(
                    **Setting.of(shift)['shift_edition_time'])
                not_assignment_time = not_assignment_time.isoformat()
                return {"editing_mode_closing": assignment_time,
                        "shift_closing": not_assignment_time}
            else:
                return None

        PERMISSIONS = []
        APP = 'all_journals_app'
        VALIDATE_CELLS = APP + ".validate_cells"
        EDIT_CELLS = APP + ".edit_cells"
        PLANT_PERM = APP + ".modify_{plant}"

        user = request.user

        if user.is_superuser:
            PERMISSIONS = ["edit", "validate"]

        elif user.has_perm(PLANT_PERM.format(plant=shift.journal.plant.name)) and \
                user.has_perm(VALIDATE_CELLS):
            PERMISSIONS.append("validate")
            if user.has_perm(EDIT_CELLS):
                PERMISSIONS.append("edit")

        else:
            if shift.closed:
                limited_emp_id_list = Setting.of(shift)["limited_access_employee_id_list"]
                if limited_emp_id_list and user.id in limited_emp_id_list:
                    PERMISSIONS = ["edit"]

            elif services.CheckRole.execute({"employee": user.employee, "page": shift}) and \
                    services.CheckTime.execute({"employee": user.employee, "page": shift}):

                if user.has_perm(PLANT_PERM.format(plant=shift.journal.plant.name)) and \
                        user.has_perm(EDIT_CELLS):
                    PERMISSIONS.append("edit")

        res = {
            "permissions": PERMISSIONS,
            "time": get_time(shift),
        }

        return res

    def journal_serializer(self, qs):
        journal = qs.journal
        res = {
            "id": journal.id,
            "name": journal.name,
            "type": journal.type,
            "tables": self.table_serializer(qs)
        }
        return res

    def table_serializer(self, qs):
        tables = qs.journal.tables.all()
        res = {
            table.name: {
                "id": table.id,
                "name": table.name,
                "title": table.verbose_name,
                "fields": self.field_serializer(qs, table), }
            for table in tables}

        return res

    def field_serializer(self, qs, table):
        fields = table.fields.all()

        res = {field.name: {
            "id": field.id,
            "name": field.name,
            "formula": field.formula,
            "field_description": {"type":field.type,
                                  "units":field.units},
            "cells": self.cell_serializer(qs, table, field)}
            for field in fields}

        return res

    def cell_serializer(self, qs, table, field):
        cells = qs.group_cells.all()
        res = {}
        for cell in cells:
            if cell.table == table and cell.field == field:
                if cell.responsible:
                    responsible = {str(cell.responsible.user): cell.responsible.name}
                else:
                    responsible = {}
                res[cell.index] = {"id": cell.id,
                                   "value": cell.value,
                                   "responsible": responsible,
                                   "created": cell.created,
                                   "comments": [{
                                       'text': comment.text,
                                       'user': {str(comment.employee.user): str(comment.employee)},
                                       'created': comment.created.isoformat()}
                                       for comment in cell.comments.all()
                                   ]
                                   }

        return res


class PrevShiftAPI(View):
    def get(self, request):
        shift_id = request.GET.get("shift_id", None)
        shift = Shift.objects.filter(id=shift_id).first()
        cellgroup = CellGroup.objects.filter(id=shift_id).first()
        journal = cellgroup.journal
        cellgroups = CellGroup.objects.filter(journal=journal)
        shifts = [Shift.objects.get(id=x.id) for x in cellgroups]
        sorted_shifts = sorted(shifts, key=lambda x : (x.date, x.order))
        prev_shift =sorted_shifts[sorted_shifts.index(shift) - 1]
        return JsonResponse(prev_shift.id, safe=False)

class PlantsAPI(View):
    def get(self, request):
        queryset = Plant.objects.all()
        res = [{"name": plant.name, "verboseName": plant.verbose_name} for plant in queryset]
        return JsonResponse(res, safe=False)


class JournalsAPI(View):
    def get(self, request):
        queryset = Journal.objects.all()
        plant = request.GET.get('plant', None)
        if plant:
            queryset = Journal.objects.filter(plant__name=plant)
        res = [{"name": journal.name, "verboseName": journal.verbose_name} for journal in queryset]
        return JsonResponse(res, safe=False)


class MenuInfoAPI(View):
    def get(self, request):
        verbose_name = {'furnace': 'Обжиг', 'electrolysis': 'Электролиз', 'leaching': 'Выщелачивание'}
        qs = Journal.objects.all()
        if str(request.user) not in ['shaukenov-s-s', 'makagonov-s-n'] and not request.user.is_superuser:
            qs = qs.exclude(name__in=['metals_compute', 'report_income_outcome_schieht'])
        return JsonResponse({
            'plants': [
                {
                    'name': plant.name,
                    'verbose_name': verbose_name[plant.name],
                    'journals': [
                        {
                            'name': journal.name,
                            'verbose_name': journal.verbose_name,
                        }
                        for journal in qs.filter(plant=plant)
                    ]
                }
                for plant in Plant.objects.all()
            ]
        })


class SettingsAPI(LoginRequired, View):
    def get(self, request):
        user = request.user.employee
        qs = Setting.objects.select_related('employee').prefetch_related('scope')

        return JsonResponse({
            "user_settings": [{"id": s.id,
                               "name": s.name,
                               "verbose_name": s.verbose_name,
                               "value": pickle.loads(s.value),
                               "content_type": ContentType.objects.get_for_model(s.scope).id,
                               "scope": model_to_dict(s.scope)} for s in qs.filter(employee=user) if s.content_type],

            "settings": [{"id": s.id,
                          "name": s.name,
                          "verbose_name": s.verbose_name,
                          "value": pickle.loads(s.value),
                          "content_type": ContentType.objects.get_for_model(s.scope).id,
                          "scope": model_to_dict(s.scope)} for s in qs if s.content_type],

            "global_settings": [{"id": s.id,
                                 "name": s.name,
                                 "verbose_name": s.verbose_name,
                                 "value": pickle.loads(s.value)} for s in
                                qs.filter(content_type=None)]
        })

    def post(self, request):
        setting_data = json.loads(request.body)
        Setting.objects.create(
            value=Setting._dumps(setting_data['value']),
            name=setting_data['name'],
            employee=request.user.employee,
            object_id=int(setting_data['scope']['id']) if setting_data.get('scope', None) else None,
            content_type=ContentType.objects.get(id=int(setting_data['content_type']))
            if setting_data.get('scope', None) else None)

        return JsonResponse({"status": 1})

    def put(self, request):
        setting_data = json.loads(request.body)
        setting = Setting.objects.get(id=int(setting_data['id']))
        setting.verbose_name = setting_data.get('value', setting.verbose_name)
        setting.value = Setting._dumps(setting_data['value'])
        setting.save()

        return JsonResponse({"status": 1})


class TablesAPI(View):
    def get(self, request):
        queryset = Table.objects.all()
        plant = request.GET.get('plant', None)
        journal = request.GET.get('journal', None)
        if plant and journal is None:
            queryset = Table.objects.filter(journal__plant__name=plant)
        elif plant and journal:
            queryset = Table.objects.filter(journal__plant__name=plant, journal__name=journal)

        res = [{"name": table.name, "verboseName": table.verbose_name} for table in queryset]
        return JsonResponse(res, safe=False)


class FieldsAPI(View):
    def get(self, request):
        queryset = Field.objects.all()
        plant = request.GET.get('plant', None)
        journal = request.GET.get('journal', None)
        table = request.GET.get('table', None)
        if plant and journal and table:
            queryset = Field.objects.filter(table__journal__plant__name=plant,
                                            table__journal__name=journal,
                                            table__name=table)
        res = [{"name": field.name, "verboseName": field.verbose_name} for field in queryset]
        return JsonResponse(res, safe=False)


class CellAPI(View):
    def get(self, request):

        shift = int(request.GET.get('shift', None))
        journal_name = request.GET.get('journal', None)
        table_name = request.GET.get('table', None)
        field_name = request.GET.get('field', None)

        journal = Journal.objects.filter(name=journal_name).first()
        table = Table.objects.filter(name=table_name, journal=journal).first()
        field = Field.objects.filter(name=field_name, table=table).first()

        field_formula = field.formula if field else None
        field_id = field.id if field else None
        if field_formula:
            value = field_formula
        else:
            cell = Cell.objects.filter(group=shift, field=field_id).first()
            value = cell.value if cell else None
        res = {"value": value}
        return JsonResponse(res, safe=False)


class SettingAPI(View):
    def get(self, request):
        # DEBUG
        # user = CustomUser.objects.get(username="inframine")
        # employee = Employee.objects.get(user=user)

        employee = request.user.employee
        name = request.GET.get("name", None)
        value = Setting.get_value(name=name, employee=employee)

        return JsonResponse({"defaultPage": value if value else ""}, safe=False)

    def post(self, request):
        # DEBUG
        # user = CustomUser.objects.get(username="inframine")
        # employee = Employee.objects.get(user=user)

        employee = request.user.employee
        setting_data = json.loads(request.body)
        Setting.set_value(name=setting_data["name"], value=setting_data["value"],
                          employee=employee, )
        return JsonResponse({"status": 1})


class AutocompleteAPI(View):
    def get(self, request):
        name = request.GET.get('name', None)
        plant = request.GET.get('plant', None)
        if name and plant:
            return JsonResponse([emp.name for emp in
                                 Employee.objects.filter(name__contains=name,
                                                         user__groups__name__contains=plant.title())],
                                safe=False)
        else:
            return JsonResponse([], safe=False)


class OpenInConstructor(View):
    def get(self, request):
        journal = request.GET.get('journal', None)
        plant = request.GET.get('plant', None)
        if journal and plant:
            try:
                copyfile(f'resources/journals/{plant}/{journal}.jrn',
                         f'e-logs-constructor/backend/media/journals/{journal}.jrn')

                return JsonResponse({"status":1})
            except:
                return JsonResponse({"status": 0})


class LoadJournalAPI(View):
    def post(self, request):
        if request.FILES.get('journal_file', None):
            journal = request.FILES['journal_file']
            plant_name = request.POST['plant']
            type = request.POST['type']
            number_of_shifts = int(request.POST['number_of_shifts'])
            if plant_name and type and number_of_shifts:
                try:
                    os.remove(f'resources/journals/{plant_name}/{journal.name}')
                except OSError:
                    pass
                fs = FileSystemStorage(location=f'resources/journals/{plant_name}/')
                filename = fs.save(journal.name, journal)

                journal = JournalBuilder(journal, plant_name, type)
                new_journal = journal.create()

                if new_journal.type == 'shift':
                    self.add_shifts(new_journal, number_of_shifts)

                return JsonResponse({"status": 1})
        return JsonResponse({"status": 0})

    @staticmethod
    def add_shifts(new_journal, number_of_shifts):
        Setting.of(obj=new_journal)['number_of_shifts'] = int(number_of_shifts)
        now_date = current_date()
        for shift_date in date_range(now_date - timedelta(days=7), now_date + timedelta(days=7)):
            for shift_order in range(1, number_of_shifts + 1):
                Shift.objects.get_or_create(journal=new_journal, order=shift_order, date=shift_date)


class ConstructorHashAPI(View):
    def post(self, request):
        journal = request.FILES['journal_file']

        fs = FileSystemStorage(location=f'resources/temp/')
        filename = fs.save(journal.name, journal)

        hasher = hashlib.md5()
        with open(f'resources/temp/{filename}', 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        journal_hash = hasher.hexdigest()
        os.rename(f'resources/temp/{filename}', f'resources/temp/{journal_hash}.jrn')

        return JsonResponse({"hash":journal_hash})


class ConstructorUploadAPI(View):
    def post(self, request):
        print(request.POST)
        hash = request.POST['hash']
        plant = request.POST['plant']
        type = request.POST['type']
        number_of_shifts = int(request.POST['number_of_shifts'])

        copyfile(f'resources/temp/{hash}.jrn',
                 f'resources/journals/{plant}/{hash}.jrn')

        journal = JournalBuilder(f'resources/journals/{plant}/{hash}.jrn', plant, type)
        new_journal = journal.create()

        if new_journal.type == 'shift':
            LoadJournalAPI.add_shifts(new_journal, number_of_shifts)

        compress_journal(journal)
        return JsonResponse({"status": 1})
