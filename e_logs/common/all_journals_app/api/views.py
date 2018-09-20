from cacheops import cached_as
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Permission
from django.views import View
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


from e_logs.common.all_journals_app.models import Plant, Journal, Table, Field, Cell, Shift
from e_logs.common.all_journals_app.services.page_modes import get_page_mode
from e_logs.core.models import Setting
from .serializers import PlantSerializer, JournalSerializer, TableSerializer, FieldSerializer, \
    CellSerializer, ShiftSerializer


class ShiftsList(generics.ListAPIView):
    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Shift.objects.all()
    filter_backends = (DjangoFilterBackend,)


class ShiftAPI(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = ShiftSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Shift.objects\
        .select_related('journal', 'journal__plant') \
        .prefetch_related('journal__plant', 'journal', 'cells', 'cells__field', 'journal__tables')\
        .all()


shift_api_view = ShiftAPI.as_view()


class ShiftAPI1(View):
    def get(self, request, *args, **kwargs):
        shift = Shift.objects.get(id=kwargs['id'])

        res = {
                "id": shift.id ,
                "plant":{"name":shift.journal.plant.name},
                "order": shift.order,
                "date": shift.date,
                "closed":shift.closed,
                "ended": shift.ended,
                "mode": get_page_mode(self.request, shift),
                "permissions": [permission.codename for permission
                    in Permission.objects.filter(user=self.request.user)],
                "journal": self.journal_serializer(shift)}

        return JsonResponse(res, safe=False)

    def journal_serializer(self, shift):
        journal = shift.journal
        res = {
                "id": journal.id,
                "name": journal.name,
                "type": journal.type,
                "tables": self.table_serializer(journal)
        }
        return res

    def table_serializer(self, journal):
        tables = Table.objects.filter(journal=journal)
        res = {
                table.name: {
                    "id": table.id,
                    "name": table.name,
                    "fields": self.field_serializer(table),}
            for table in tables}

        return res

    def field_serializer(self, table):
        fields = Field.objects.filter(table=table)

        res = {field.name: {
                        "id": field.id,
                        "name": field.name,
                        "field_description": Setting.of(field)['field_description'],
                        "cells": self.cell_serializer(field)}
            for field in fields }

        return res

    def cell_serializer(self, field):
        cells = Cell.objects.filter(field=field)
        res = {
            cell.index:{
            "id":cell.id,
            "value":cell.value}
                    for cell in cells}

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


class CellsList(generics.ListAPIView):
    serializer_class = CellSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Cell.objects.all()

    def post(self, request):
        return Response({"detail": "Hello, !"}, status=status.HTTP_200_OK)

    # filter_backends = (DjangoFilterBackend,)
    # filter_fields = (
    #     'field__table__journal__plant__name', 'field__table__journal__name', 'field__table__name',
    #     'field__name', 'group_id')


class CellAPI(generics.RetrieveAPIView):
    lookup_field = 'id'
    serializer_class = CellSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Cell.objects.all()
