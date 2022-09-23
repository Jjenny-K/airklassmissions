from rest_framework import serializers

from contentshub.models import Master, Klass


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'name',
            'description',
        )


class KlassSerializer(serializers.ModelSerializer):
    master = serializers.ReadOnlyField(source='master.name')

    class Meta:
        model = Klass
        fields = (
            'master',
            'title',
            'description',
            'created_at',
        )
        read_only_fields = (
            'created_at',
        )
