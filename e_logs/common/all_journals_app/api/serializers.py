from collections import OrderedDict

from rest_framework import serializers
from rest_framework.fields import SkipField

from e_logs.common.all_journals_app.models import Plant, Cell, Table, Journal, Field, Shift
from e_logs.core.api.utils import cached


class CellSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cell
        fields = ("id", "index", "value")


class FieldSerializer(serializers.ModelSerializer):
    cells = serializers.SerializerMethodField("get_cell")

    def get_cell(self, obj):

        return self.context.get('shift_id')

    class Meta:
        model = Field
        fields = ('id', "name", "cells")


class TableSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)


    def get_journal_name(self, obj):
        return obj.journal.name

    class Meta:
        model = Table
        fields = ('id', "name", 'fields')


class JournalSerializer(serializers.ModelSerializer):
    tables = TableSerializer(many=True)


    def get_plant_name(self, obj):
        return obj.plant.name

    class Meta:
        model = Journal
        fields = ('id', 'name','type','tables')

class ShiftSerializer(serializers.ModelSerializer):
    journal = serializers.SerializerMethodField('serialize_shift')

    def serialize_shift(self, obj):
        return JournalSerializer(instance=Journal.objects.get(cellgroup=obj),
                                 context={"shift_id":obj.id}).data

    class Meta:
        model = Shift
        fields = ('id', 'order', 'date', 'journal')


class PlantSerializer(serializers.ModelSerializer):
    journals = JournalSerializer(many=True)

    class Meta:
        model = Plant
        fields = ('id', 'name', 'journals')
