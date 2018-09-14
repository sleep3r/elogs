from rest_framework import serializers

from ..models import Setting


class SettingSerializer(serializers.ModelSerializer):
    # journals = JournalSerializer(many=True)

    class Meta:
        model = Setting
        fields = "__all__"
