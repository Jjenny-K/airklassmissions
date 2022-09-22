from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from contentshub.models import Master
from contentshub.serializers import MasterSerializer
from contentshub.permissions import IsMasterOrReadOnly
from accounts.models import User


class MasterViewSet(viewsets.ModelViewSet):
    """
        로그인된 정보를 통해 사용자 정보 등록
        pk값 입력을 통한 강사 정보 접근

        인증받은 사용자의 본인의 정보가 아닐 경우 강사 정보 접근 불가
    """

    queryset = Master.objects.all()
    serializer_class = MasterSerializer
    permission_classes = (IsMasterOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 로그인된 사용자 정보를 추가해 Master 틍록
            Master.objects.create(
                user_id=request.user.id,
                name=request.data['name'],
                description=request.data['description'],
            )

            # 해당 사용자의 is_master를 True로 지정해 강사 여부 업데이트
            user = User.objects.get(id=request.user.id)
            user.is_master = True
            user.save(update_fields=['is_master'])

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, *args, **kwargs):
        # 로그인된 사용자 본인이 등록한 강사 정보만 조회
        query = Q(user=request.user)
        self.queryset = self.get_queryset().filter(query)

        return super().list(request, *args, **kwargs)
