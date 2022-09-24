from rest_framework import serializers

from contentshub.models import Master, Klass
from community.models import Question, Answer


class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = (
            'name',
            'description',
        )


class KlassListSerializer(serializers.ModelSerializer):
    """ 강의 리스트 조회 serializer """
    master = serializers.ReadOnlyField(source='master.name')

    class Meta:
        model = Klass
        fields = (
            'master',
            'title',
            'created_at',
        )
        read_only_fields = (
            'title',
            'created_at',
        )


class AnswerPreviewSerializer(serializers.ModelSerializer):
    """ 답변 미리보기 serializer """
    class Meta:
        model = Answer
        fields = (
            'contents',
            'created_at',
        )
        read_only_fields = (
            'contents',
            'created_at',
        )


class QuestionAnswerPreviewSerializer(serializers.ModelSerializer):
    """ 질문, 답변 미리보기 serializer """
    question_writer = serializers.ReadOnlyField(source='user.username')
    answer = AnswerPreviewSerializer(read_only=True)

    class Meta:
        model = Question
        fields = (
            'question_writer',
            'contents',
            'created_at',
            'answer'
        )
        read_only_fields = (
            'contents',
            'created_at',
        )


class KlassSerializer(serializers.ModelSerializer):
    master = serializers.ReadOnlyField(source='master.name')
    questions = QuestionAnswerPreviewSerializer(many=True, read_only=True)

    class Meta:
        model = Klass
        fields = (
            'master',
            'title',
            'description',
            'created_at',
            'questions',
        )
        read_only_fields = (
            'created_at',
        )
