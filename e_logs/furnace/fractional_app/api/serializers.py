from django.utils import timezone

from rest_framework import serializers

from e_logs.common.all_journals_app.models import Plant, Measurement, Cell
from e_logs.core.api import cached


class MeasurementSerializer(serializers.Serializer):
    id              = serializers.IntegerField(read_only=True)
    time            = serializers.DateTimeField(default=timezone.now())
    cinder_masses   = serializers.ListField(child=serializers.FloatField(), min_length=1)
    schieht_masses  = serializers.ListField(child=serializers.FloatField(), min_length=1)
    cinder_sizes    = serializers.ListField(child=serializers.FloatField(), min_length=1)
    schieht_sizes   = serializers.ListField(child=serializers.FloatField(), min_length=1)

    @cached('measurement')
    def to_representation(self, instance):
        return super().to_representation(instance)

    def create(self, validated_data):
        measurement = Measurement.objects.create(type="measurement",
                                                 time = validated_data["time"],
                                                 name = "fractional_anal",
                                                 plant=Plant.objects.get(name="furnace"))
        self._save(validated_data, measurement)


    def update(self, instance, validated_data):
        measurement = instance
        Cell.objects.filter(group=measurement).delete()

        self._save(validated_data, measurement)

    def _save(self, validated_data, measurement):
        for i, m_value in enumerate(validated_data["cinder_masses"]):
            Cell.objects.create(table_name="measurements", field_name='cinder_mass',
                                index=i, value=round(float(m_value), 2), group=measurement)
        for i, m_value in enumerate(validated_data["cinder_sizes"]):
            Cell.objects.create(table_name="measurements", field_name='cinder_size',
                                index=i, value=round(float(m_value), 2), group=measurement)
        for i, m_value in enumerate(validated_data["schieht_masses"]):
            Cell.objects.create(table_name="measurements", field_name='schieht_mass',
                                index=i, value=round(float(m_value), 2), group=measurement)
        for i, m_value in enumerate(validated_data["schieht_sizes"]):
            Cell.objects.create(table_name="measurements", field_name='schieht_size',
                                index=i, value=round(float(m_value), 2), group=measurement)

class MeasurementGraphsSerializer(serializers.Serializer):
    cinder   = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))
    schieht  = serializers.ListField(child=serializers.ListField(child=serializers.FloatField()))


#Some funnyn't serializers frac_anal_app modelserializing

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