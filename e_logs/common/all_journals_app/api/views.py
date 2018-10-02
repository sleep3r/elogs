import pickle
from urllib.parse import parse_qs

from cacheops import cached_as
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.db import transaction
from django.db.models import Prefetch
from django.forms import model_to_dict
from django.shortcuts import render_to_response
from django.views import View
from django.http import JsonResponse


from e_logs.common.all_journals_app.models import Plant, Journal, Table, Field, Shift, Cell
from e_logs.common.all_journals_app.views import get_current_shift
from e_logs.common.all_journals_app.services.page_modes import get_page_mode
from e_logs.common.login_app.models import Employee
from e_logs.core.models import Setting


class ShiftAPI(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if not kwargs.get('id', None):
            journal_name = parse_qs(request.GET.urlencode())['journalName'][0]
            current_shift = get_current_shift(Journal.objects.get(name=journal_name))
            if current_shift:
                id = current_shift.id
            else:
                id = Shift.objects.latest('date').id
        else:
            id = kwargs['id']
        qs = Shift.objects\
        .select_related('journal', 'journal__plant') \
        .prefetch_related('journal__tables', 'journal__tables__fields',
                          Prefetch('journal__tables__fields__settings',
                                    queryset=Setting.objects.filter(name='field_description')),
                          Prefetch('group_cells',
                                   queryset=Cell.objects.select_related('field', 'field__table').
                                   filter(group_id=id)),
                          ).get(id=id)
        plant = qs.journal.plant
        res = {
                "id": qs.id ,
                "plant":{"name":plant.name},
                "order": qs.order,
                "date": qs.date,
                "closed":qs.closed,
                "ended": qs.ended,
                "mode": get_page_mode(user=user, plant=plant),
                "permissions": [permission.codename for permission
                    in Permission.objects.filter(user=user)],
                "journal": self.journal_serializer(qs)}
        return JsonResponse(res, safe=False)

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
                    "fields": self.field_serializer(qs, table),}
            for table in tables}

        return res

    def field_serializer(self, qs, table):
        fields = table.fields.all()

        res = {field.name: {
                        "id": field.id,
                        "name": field.name,
                        "field_description": pickle.loads(list(field.settings.all())[-1].value)
                                if field.settings.all() else '',
                        "cells": self.cell_serializer(qs, table, field)}
            for field in fields }

        return res

    def cell_serializer(self, qs, table, field):
        cells = qs.group_cells.all()
        res = {}
        for cell in cells:
            if cell.table == table and cell.field == field:
                res[cell.index] = {"id":cell.id, "value":cell.value}

        return res

class PlantAPI(LoginRequiredMixin ,View):
    def get(self, request):
        queryset = Plant.objects.all()
        res = [{plant.name:plant.verbose_name} for plant in queryset]
        return JsonResponse(res, safe=False)


class JournalAPI(View):
    def get(self, request):
        queryset = Journal.objects.all()
        plant = request.GET.get('plant', None)
        if plant:
            queryset = Journal.objects.filter(plant__name=plant)
        res = [{journal.name:journal.verbose_name} for journal in queryset]
        return JsonResponse(res, safe=False)


class MenuInfoAPI(View):
    def get(self, request):
        verbose_name = {'furnace': 'Обжиг', 'electrolysis': 'Электролиз', 'leaching': 'Выщелачивание'}
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
                    for journal in Journal.objects.filter(plant=plant)
                    ]
                }
                for plant in Plant.objects.all()
            ]
        })


class SettingsAPI(View):
    def get(self, request):
        user = request.user.employee
        qs = Setting.objects.select_related('employee').prefetch_related('scope')

        return JsonResponse({
            "user_settings": [{"name":s.name,
                               "value":pickle.loads(s.value),
                               "scope":model_to_dict(s.scope)} for s in qs.filter(employee=user)],

            "settings":[{"name":s.name,
                         "value":pickle.loads(s.value),
                         "scope":model_to_dict(s.scope)} for s in qs],
        })


class TableAPI(View):
    def get(self, request):
        queryset = Table.objects.all()
        plant = request.GET.get('plant', None)
        journal = request.GET.get('journal', None)
        if plant and journal is None:
            queryset = Table.objects.filter(journal__plant__name=plant)
        elif plant and journal:
            queryset = Table.objects.filter(journal__plant__name=plant, journal__name = journal)

        res = [{table.name:table.verbose_name} for table in queryset]
        return JsonResponse(res, safe=False)


class FieldAPI(View):
    def get(self, request):
        queryset = Field.objects.all()
        plant = request.GET.get('plant', None)
        journal = request.GET.get('journal', None)
        table = request.GET.get('table', None)
        if plant and journal and table:
            queryset = Field.objects.filter(table__journal__plant__name=plant,
                                            table__journal__name=journal,
                                            table__name=table)
        res = [{field.name:field.verbose_name} for field in queryset]
        return JsonResponse(res, safe=False)


class AutocompleteAPI(View):
    def get(self, request):
        name = request.GET.get('name', None)
        if name:
            return JsonResponse([emp.name for emp in Employee.objects.filter(name__contains=name)],
                                safe=False)
        else:
            return JsonResponse([], safe=False)
