from rest_framework import serializers

from e_logs.common.all_journals_app.models import Plant, Cell, Table, Journal, Field
from e_logs.core.api import cached


class CellSerializer(serializers.ModelSerializer):

    @cached('cell')
    def to_representation(self, instance):
        return super().to_representation(instance)

    class Meta:
        model = Cell
        fields = ("id", "index", "value")


class FieldSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True)
    table = serializers.SerializerMethodField('get_table_name')

    @cached('field')
    def to_representation(self, instance):
        return super().to_representation(instance)

    def get_table_name(self, obj):
        return obj.table.name

    class Meta:
        model = Field
        fields = ('id', "name", "table", "cells")


class TableSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)
    journal = serializers.SerializerMethodField('get_journal_name')

    @cached('table')
    def to_representation(self, instance):
        return super().to_representation(instance)

    def get_journal_name(self, obj):
        return obj.journal.name

    class Meta:
        model = Table
        fields = ('id', "name", 'journal', 'fields')


class JournalSerializer(serializers.ModelSerializer):
    tables = TableSerializer(many=True)
    plant = serializers.SerializerMethodField('get_plant_name')

    @cached('journal')
    def to_representation(self, instance):
        return super().to_representation(instance)

    def get_plant_name(self, obj):
        return obj.plant.name

    class Meta:
        model = Journal
        fields = ('id', 'name', 'type', 'plant', 'tables',)


class PlantSerializer(serializers.ModelSerializer):
    journals = JournalSerializer(many=True)

    @cached('plant')
    def to_representation(self, instance):
        return super().to_representation(instance)

    class Meta:
        model = Plant
        fields = ('id', 'name', 'journals')
