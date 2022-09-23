from rest_framework import serializers

from community.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    klass_title = serializers.ReadOnlyField(source='klass.title')
    klass_master = serializers.ReadOnlyField(source='klass.master.name')
    answer = serializers.SlugRelatedField(slug_field='contents', read_only=True, allow_null=True)

    class Meta:
        model = Question
        fields = (
            'username',
            'klass',
            'klass_title',
            'klass_master',
            'contents',
            'answer',
        )
        extra_kwargs = {
            'klass': {'write_only': True}
        }
