from cacheops import cached_as
from rest_framework import serializers

from django.contrib.auth.models import Permission

from e_logs.common.all_journals_app.services.page_modes import get_page_mode, has_edited, \
    plant_permission
from e_logs.common.all_journals_app.models import Plant, Cell, Table, Journal, Field, Shift, \
    CellGroup
from e_logs.core.models import Setting

class CellSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cell
        fields = ("id", "index", "value")


class ShiftSerializer(serializers.ModelSerializer):
    journal = serializers.SerializerMethodField('serialize_shift')
    mode = serializers.SerializerMethodField('get_page_mode')
    permissions = serializers.SerializerMethodField()
    plant = serializers.SerializerMethodField()

    def get_plant(self, obj):
        return {'name': obj.journal.plant.name}

    def get_page_mode(self, obj):
        return get_page_mode(self.context['request'], obj)

    def get_permissions(self, obj):
        return [permission.codename for permission
                    in Permission.objects.filter(user=self.context['request'].user)]

    @cached_as(Shift, Cell, CellGroup)
    def serialize_shift(self, obj):
        serializer = JournalSerializer(instance=Journal.objects.get(cellgroup=obj),
                                       context={"shift_id": obj.id})
        return serializer.data

    class Meta:
        model = Shift
        fields = ("id", "order", "date", "mode", "permissions", "journal", "plant")


class FieldSerializer(serializers.ModelSerializer):
    cells = serializers.SerializerMethodField("get_cell")
    field_description = serializers.SerializerMethodField()

    def get_field_description(self, obj):
        return Setting.of(obj)['field_description']

    def get_cell(self, obj):
        qs = Cell.objects.filter(group_id=self.context.get('shift_id'), field=obj)
        return {str(CellSerializer(c).data.get('index')): CellSerializer(c).data for c in qs}

    class Meta:
        model = Field
        fields = ('id', "name", "field_description", "cells")


class TableSerializer(serializers.ModelSerializer):
    fields = serializers.SerializerMethodField('get_fields_dict')

    def get_fields_dict(self, obj):
        return {FieldSerializer(f).data.get('name'):
                FieldSerializer(f, context={"shift_id": self.context.get('shift_id')}).data
                for f in obj.fields.all()}

    class Meta:
        model = Table
        fields = ('id', 'name', 'fields', )


class JournalSerializer(serializers.ModelSerializer):
    tables = serializers.SerializerMethodField()

    def get_tables(self, obj):
        return {TableSerializer(t).data.get('name'):
                TableSerializer(t, context={"shift_id": self.context.get('shift_id')}).data
                for t in obj.tables.all()}

    class Meta:
        model = Journal
        fields = ('id', 'name', 'type', 'tables',)


class PlantSerializer(serializers.ModelSerializer):
    journals = JournalSerializer(many=True)

    class Meta:
        model = Plant
        fields = ("id", "name", "journals")
