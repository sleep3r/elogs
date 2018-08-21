from rest_framework import serializers

from e_logs.common.all_journals_app.models import Plant, Cell, Table, Journal, Field, Shift
from e_logs.core.api.utils import cached


class FilteredListSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        data = data.filter(group__id=self.context.get('shift_id'))
        return super(FilteredListSerializer, self).to_representation(data)


class CellSerializer(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = FilteredListSerializer
        model = Cell
        fields = ("id", "index", "value")


class ShiftSerializer(serializers.ModelSerializer):

    journal = serializers.SerializerMethodField()

    def get_journal(self, obj):
        journal = obj.journal
        context = {'request': self.context.get('request'), 'shift_id': obj.id}
        serializer = JournalSerializer(journal, context=context)
        return serializer.data

    class Meta:
        model = Shift
        fields = ("id", "order", "date", "journal")


class FieldSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True)

    class Meta:
        model = Field
        fields = ('id', "name", "cells")


class TableSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True)
    journal = serializers.SerializerMethodField('get_journal_name')


    def get_journal_name(self, obj):
        return obj.journal.name

    class Meta:
        model = Table
        fields = ('id', "name", 'journal', 'fields')


class JournalSerializer(serializers.ModelSerializer):
    tables = TableSerializer(many=True)
    plant = serializers.SerializerMethodField('get_plant_name')


    def get_plant_name(self, obj):
        return obj.plant.name

    class Meta:
        model = Journal
        fields = ('id', 'name', 'type', 'plant', 'tables',)


class PlantSerializer(serializers.ModelSerializer):
    journals = JournalSerializer(many=True)

    class Meta:
        model = Plant
        fields = ('id', 'name', 'journals')
