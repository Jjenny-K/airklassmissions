from rest_framework import viewsets, status
from rest_framework.response import Response

from community.models import Question
from community.serializers import QuestionSerializer
from community.permissions import QuestionIsOwnerOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    """
        로그인된 정보를 통해 사용자 정보 등록
        pk값 입력을 통한 질문 정보 접근

        인증받은 사용자의 본인이 작성한 질문이 아닐 경우 질문 조회, 수정, 삭제 접근 불가
    """

    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
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
