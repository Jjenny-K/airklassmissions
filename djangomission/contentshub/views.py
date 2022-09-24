from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.response import Response

from contentshub.models import Master, Klass
from contentshub.serializers import MasterSerializer, KlassSerializer, KlassListSerializer
from contentshub.permissions import IsMasterOrReadOnly, KlassIsMasterOrReadOnly
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
            try:
                # 로그인된 사용자 정보를 추가해 Master 틍록
                Master.objects.create(
                    user_id=request.user.id,
                    name=request.data['name'],
                    description=request.data['description'],
                )
            except:
                # 입력된 데이터에 해당하는 사용자가 강사로 등록되어 있을 경우 예외처리
                return Response({'message': '이미 등록된 강사입니다.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
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


class KlassViewSet(viewsets.ModelViewSet):
    """
        로그인된 정보를 통해 강사 정보 등록
        pk값 입력을 통한 강의 정보 접근

        인증받은 사용자 본인이 강사가 아닐 경우, 강의 등록 불가
        인증받은 사용자 본인이 생성한 강의가 아닐 경우 강의 정보 상세조회, 수정, 삭제 접근 불가
    """

    queryset = Klass.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return KlassListSerializer
        else:
            return KlassSerializer

    permission_classes = (KlassIsMasterOrReadOnly,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # 로그인된 사용자 정보를 통해 Klass 틍록
            master = Master.objects.get(user=request.user)

            Klass.objects.create(
                master_id=master.id,
                title=request.data['title'],
                description=request.data['description'],
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
