from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.models import User
from accounts.serializers import UserSignupSerializer, \
                                 UserLoginSerializer, \
                                 UserLogoutSerializer, \
                                 UserSerializer


class UserViewset(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    """
        email, username, password 입력을 통한 회원가입
        로그인 시 access_token, refresh_token 부여, refresh_token 쿠키 저장
        pk값 입력을 통한 사용자 정보 접근
        쿠키 내 refresh_token 제거를 통한 로그아웃
    """

    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'signup':
            return UserSignupSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        elif self.action == 'logout':
            return UserLogoutSerializer
        else:
            return UserSerializer

    @action(methods=['post'], detail=False)
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response({'message': f'{serializer.data["username"]}님 가입을 환영합니다.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            response = Response(status=status.HTTP_200_OK)
            response.data = {'user': serializer.validated_data['user'].email,
                             'access_token': serializer.validated_data['access_token']}

            # 로그인 시 refresh_token 쿠키 저장
            response.set_cookie(key='refresh_token', value=serializer.validated_data['refresh_token'], httponly=True)

            return response

    @action(methods=['post'], detail=False)
    def logout(self, request):
        response = Response({'message': '로그아웃 되었습니다.'}, status=status.HTTP_202_ACCEPTED)

        # 쿠키에서 refresh_token을 제거하여 로그아웃
        response.delete_cookie('refresh_token')

        return response
