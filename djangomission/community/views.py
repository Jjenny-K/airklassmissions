from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from community.models import Question, Answer
from community.serializers import QuestionCreateSerializer, \
                                  QuestionListSerializer, \
                                  QuestionSerializer, \
                                  AnswerSerializer
from community.permissions import QuestionIsOwnerOrReadOnly, \
                                  QuestionDestroyIsOwnerIsMaster, \
                                  AnswerIsMasterOrReadOnly


class QuestionViewSet(viewsets.ModelViewSet):
    """
        로그인된 정보를 통해 사용자 정보 등록
        pk값 입력을 통한 질문 정보 접근
        답변이 등록된 질문의 경우 삭제 불가

        인증받은 사용자 본인이 작성한 질문이 아닐 경우 질문 조회, 수정 접근 불가
        인증받은 사용자 본인이 작성한 질문이 아닐 경우, 질문이 작성된 강의의 강사가 아닐 경우 삭제 접근 불가
    """

    def get_queryset(self):
        if self.action == 'answers':
            return Answer.objects.all()
        else:
            return Question.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return QuestionCreateSerializer
        elif self.action == 'list':
            return QuestionListSerializer
        elif self.action == 'answers':
            return AnswerSerializer
        else:
            return QuestionSerializer

    def get_permissions(self):
        if self.action == 'answers':
            permission_classes = (AnswerIsMasterOrReadOnly,)
        elif self.action == 'destroy':
            permission_classes = (QuestionDestroyIsOwnerIsMaster,)
        else:
            permission_classes = (QuestionIsOwnerOrReadOnly,)

        return [permission() for permission in permission_classes]

    def get_answer(self, pk):
        return get_object_or_404(Answer, question_id=pk)

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

    def destroy(self, request, *args, **kwargs):
        question = self.get_object()

        try:
            self.get_answer(question.id)
        except:
            # 입력된 데이터에 해당하는 질문에 답변이 등롣되어 있지 않은 경우 삭제
            return super().destroy(request, *args, **kwargs)
        else:
            # 입력된 데이터에 해당하는 질문에 답변이 등록되어 있는 경우 예외처리
            return Response({'message': '답변이 등록된 질문은 삭제할 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get', 'post', 'delete'], detail=True)
    def answers(self, request, pk, *args, **kwargs):
        """
            pk값을 통해 답변 정보 등록

            인증받은 사용자의 본인이 등록한 강의의 질문이 아닐 경우 답변 정보 접근 불가
        """
        if request.method == 'GET':
            return super().list(request, *args, **kwargs)
        elif request.method == 'POST':
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                try:
                    # pk값으로 질문 정보를 추가해 Answer 틍록
                    Answer.objects.create(
                        question_id=pk,
                        contents=request.data['contents'],
                    )
                except:
                    # 입력된 데이터에 해당하는 질문에 답변이 등록되어 있을 경우 예외처리
                    return Response({'message': '이미 등록된 답변이 있습니다.'}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            answer = self.get_answer(pk)

            if answer is not None:
                answer.delete()

                return Response({'message': '답변이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

            return Response({'message': '작성된 답변이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)
