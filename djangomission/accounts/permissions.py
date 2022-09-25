from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        인증받은 사용자의 경우 사용자 정보 조회 허용
        인증받은 사용자 본인의 정보가 아닐 경우 상세조회, 수정, 삭제 제한
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.COOKIES.get('refresh_token'):
            if hasattr(obj, 'email'):
                return obj.email == request.user.email
            else:
                return False

        return False
