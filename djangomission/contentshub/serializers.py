from rest_framework import serializers

from contentshub.models import Master


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'name',
            'description',
        )
