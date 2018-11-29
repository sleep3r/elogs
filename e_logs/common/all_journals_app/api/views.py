import json
import os
import pickle
import hashlib
from datetime import timedelta
from shutil import copyfile
from urllib.parse import parse_qs
from collections import defaultdict

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
from e_logs.common.all_journals_app.views import _get_current_group
from e_logs.common.all_journals_app.services.page_modes import get_page_mode
from e_logs.common.login_app.models import Employee
from e_logs.core.models import Setting
from e_logs.core.utils.webutils import current_date, date_range, user_to_response
from e_logs.core.views import LoginRequired
from e_logs.core.management.commands.compress_journals import compress_journal


class GroupAPI(LoginRequired, View):
    def get(self, request, *args, **kwargs):
        group, id = self.get_current_group(request, kwargs)
        qs = group.objects.select_related('journal', 'journal__plant') \
            .prefetch_related('journal__tables', 'journal__tables__fields',
                              Prefetch('group_cells', queryset=Cell.objects.select_related(
                                  'field',
                                  'field__table',
                                  'responsible__user',
                                  'responsible').
                                       filter(group_id=id).prefetch_related(
                                  Prefetch('comments', queryset=Comment.objects.all().select_related('employee__user',
                                                                                                     'employee'))))). \
            get(id=id)

        res = self.get_context(request, qs)

        self.add_constraints(qs, res)

        return JsonResponse(res, safe=False)

    def get_context(self, request, qs):
        plant = qs.journal.plant
        user = request.user
        res = {
            "id": qs.id,
            "plant": {"name": plant.name},
            "version":qs.version,
            "mode": get_page_mode(user=user, plant=plant),
            "field_constraints_modes": self.constraint_modes_serializer(qs),
            "journal": self.journal_serializer(qs),
            "permissions": self.get_permissions(request, qs)}

        if qs.journal.type == 'shift':
            res.update(
                {"order": qs.order,
                 "date": qs.date.isoformat(),
                 'start_time': qs.start_time.isoformat(),
                 "closed": qs.closed,
                 "responsibles": [{str(e.user): str(e)} for e in qs.responsibles.all()],
                 }
            )
        elif qs.journal.type == 'year' or qs.journal.type == 'month':
            res.update(
                {"year": qs.year_date,
                 "month": qs.month_date if hasattr(qs, 'month_date') else None}
            )
        elif qs.journal.type == 'equipment':
            res.update(
                {"equipment": qs.name, }
            )

        return res

    def constraint_modes_serializer(self, qs):
        return {
            "modes": [{
                "id": mode.id,
                "is_active": mode.is_active,
                "message": mode.message,
            } for mode in Mode.objects.filter(journal=qs.journal)
            ]
        }

    def add_constraints(self, qs, res):
        modes = Mode.objects.filter(journal=qs.journal).order_by('beginning')
        if modes.exists():
            # mode = modes.last()

            for mode in modes:
                constraints = FieldConstraints.objects.filter(mode=mode)
                for constraint in constraints:
                    field = constraint.field
                    desc = res['journal']['tables'][field.table.name]['fields'][field.name][
                        'field_description']
                    desc['constraints_modes'] = {
                        mode.id: {
                            'min_normal': constraint.min_normal,
                            'max_normal': constraint.max_normal
                        }
                    }

    def get_current_group(self, request, kwargs):
        if not kwargs.get('id', None):
            journal_name = parse_qs(request.GET.urlencode())['journalName'][0]
            plant_name = parse_qs(request.GET.urlencode())['plantName'][0]
            current_group = _get_current_group(Journal.objects.get(name=journal_name, plant__name=plant_name))
            id = current_group.id
        else:
            id = kwargs['id']
        group = CellGroup.objects.get(id=id).journal.group

        return group, id

    def get_permissions(self, request, group):
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

        if group.journal.type == 'shift':
            shift = group

            if user.has_perm(PLANT_PERM.format(plant=shift.journal.plant.name)) and \
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
        else:
            res = {
                "permissions": ["edit"] if user.has_perm(
                    PLANT_PERM.format(plant=group.journal.plant.name)) else [],
                "time": None,
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
            "title": field.verbose_name,
            "formula": field.formula,
            "field_description": {"type": field.type,
                                  "units": field.units},
            "cells": self.cell_serializer(qs, table, field)}
            for field in fields}

        return res

    def cell_serializer(self, qs, table, field):
        cells = qs.group_cells.all()
        res = {}
        for cell in cells:
            if cell.table == table and cell.field == field:
                if cell.responsible:
                    responsible = user_to_response(cell.responsible)
                else:
                    responsible = {}
                res[cell.index] = {
                    "id": cell.id,
                    "value": cell.value,
                    "responsible": responsible,
                    "created": cell.created,
                    "comments": [{
                        'text': comment.text,
                        'user': user_to_response(comment.employee),
                        'type': comment.type,
                        'created': comment.created.isoformat()}
                        for comment in cell.comments.all()]
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
        sorted_shifts = sorted(shifts, key=lambda x: (x.date, x.order))
        prev_shift = sorted_shifts[sorted_shifts.index(shift) - 1]
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
        qs = Journal.objects.all()
        if str(request.user) not in ['шаукенов-ш-с', 'макагонов-с-н'] and not request.user.is_superuser:
            qs = qs.exclude(name__in=['metals_compute', 'report_income_outcome_schieht'])
        return JsonResponse({
            'plants': [
                {
                    'name': plant.name,
                    'verbose_name': plant.verbose_name,
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

        return JsonResponse(dict(name=value if value else ""), safe=False)

    def post(self, request):
        # DEBUG
        # user = CustomUser.objects.get(username="inframine")
        # employee = Employee.objects.get(user=user)

        employee = request.user.employee
        setting_data = json.loads(request.body)
        Setting.set_value(name=setting_data["name"], value=setting_data["value"], employee=employee)
        return JsonResponse({"status": 1})


class SchemeAPI(View):
    def get(self, request):
        res = {}
        journals = Journal.objects.all()
        for journal in journals:
            tables = Table.objects.filter(journal=journal)
            journal_dict = defaultdict(list)
            for table in tables:
                fields = Field.objects.filter(table=table)
                for field in fields:
                    journal_dict[table.name].append(field.name)
            res[journal.name] = journal_dict
        return JsonResponse(res)

