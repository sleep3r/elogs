from django.utils import timezone

from rest_framework import serializers

from e_logs.common.all_journals_app.models import Measurement, Cell, Table, Journal, Field
from e_logs.core.api import cached


class MeasurementSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(default=timezone.now())
    cinder_masses = serializers.ListField(child=serializers.FloatField(), min_length=1)
    schieht_masses = serializers.ListField(child=serializers.FloatField(), min_length=1)
    cinder_sizes = serializers.ListField(child=serializers.FloatField(), min_length=1)
    schieht_sizes = serializers.ListField(child=serializers.FloatField(), min_length=1)

    @cached('measurement')
    def to_representation(self, instance):
        return super().to_representation(instance)

    def create(self, validated_data):
        measurement = Measurement.objects.create(time=validated_data["time"],
                                                 name="fractional_anal",
                                                 journal=
                                                 Journal.objects.get_or_create(name="fractional")[
                                                     0])
        self._save(validated_data, measurement)

    def update(self, instance, validated_data):
        measurement = instance
        Cell.objects.filter(group=measurement).delete()
        self._save(validated_data, measurement)

    @staticmethod
    def _save(validated_data, measurement):
        journal = Journal.objects.get_or_create(name="fractional")[0]
        table = Table.objects.get_or_create(journal=journal, name='measurements')[0]

        fields = [("cinder_masses", 'cinder_mass'), ("cinder_sizes", 'cinder_size'),
                  ("schieht_masses", 'schieht_mass'), ("schieht_sizes", 'schieht_size')]

        for data, field_name in fields:
            for i, m_value in enumerate(validated_data[data]):
                Cell.objects.create(
                    field=Field.objects.get_or_create(name=field_name, table=table)[0],
                    index=i, value=round(float(m_value), 2), group=measurement)


class MeasurementGraphsSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    cinder = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))
    schieht = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))

# Some funnyn't serializers frac_anal_app modelserializing

# class HuySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cell
#         fields = ('field_name', 'value')
#
# class PidorSerializer(serializers.ModelSerializer):
#     data = HuySerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Measurement
#         fields = ('id', 'time', 'data')
