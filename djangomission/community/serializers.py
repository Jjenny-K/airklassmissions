from rest_framework import serializers

from community.models import Question, Answer


class QuestionCreateSerializer(serializers.ModelSerializer):
    """ 질문 등록 serializer """
    class Meta:
        model = Question
        fields = (
            'klass',
            'contents',
        )


class QuestionListSerializer(serializers.ModelSerializer):
    """ 질문 리스트 조회 serializer """
    username = serializers.ReadOnlyField(source='user.username')
    klass_title = serializers.ReadOnlyField(source='klass.title')
    answer_count = serializers.SerializerMethodField('get_answer_count')

    class Meta:
        model = Question
        fields = (
            'username',
            'klass_title',
            'contents',
            'created_at',
            'answer_count',
        )
        read_only_fields = (
            'created_at',
        )

    def get_answer_count(self, obj):
        return Answer.objects.filter(question_id=obj.id).count()


class QuestionSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    klass_title = serializers.ReadOnlyField(source='klass.title')
    klass_master = serializers.ReadOnlyField(source='klass.master.name')
    answer = serializers.SlugRelatedField(slug_field='contents', read_only=True, allow_null=True)

    class Meta:
        model = Question
        fields = (
            'username',
            'klass_title',
            'klass_master',
            'contents',
            'created_at',
            'answer',
        )
        read_only_fields = (
            'created_at',
        )
