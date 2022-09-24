from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from community.models import Question
from community.serializers import QuestionCreateSerializer, \
                                  QuestionListSerializer, \
                                  QuestionSerializer
from community.permissions import QuestionIsOwnerOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    """
        로그인된 정보를 통해 사용자 정보 등록
        pk값 입력을 통한 질문 정보 접근

        인증받은 사용자의 본인이 작성한 질문이 아닐 경우 질문 조회, 수정, 삭제 접근 불가
    """

    queryset = Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializer
        elif self.action == 'list':
            return QuestionListSerializer
        else:
            return QuestionSerializer

    permission_classes = (QuestionIsOwnerOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 로그인된 사용자 정보를 추가해 Question 틍록
            Question.objects.create(
                user_id=request.user.id,
                klass_id=request.data['klass'],
                contents=request.data['contents'],
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # 로그인된 사용자 본인이 등록한 질문 정보만 조회
        query = Q(user=request.user)
        self.queryset = self.get_queryset().filter(query)

        return super().list(request, *args, **kwargs)
