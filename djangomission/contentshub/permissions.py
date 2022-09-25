from rest_framework import permissions


class IsMasterOrReadOnly(permissions.BasePermission):
    """
        인증받은 사용자 본인의 정보가 아닐 경우 권한 제한
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.COOKIES.get('refresh_token'):
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.COOKIES.get('refresh_token'):
            if hasattr(obj.user, 'email'):
                return obj.user.email == request.user.email
            else:
                return False

        return False


class KlassIsMasterOrReadOnly(permissions.BasePermission):
    """
        강의 조회는 모든 사용자에게 허용
        인증받은 사용자 본인이 강사가 아닐 경우 강의 등록 제한
        인증받은 사용자 본인이 등록한 강의가 아닐 경우 수정, 삭제 제한
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            # GET, HEAD, OPTIONS 요청의 경우 허용
            return True

        if request.user.is_authenticated and request.COOKIES.get('refresh_token') and request.user.is_master:
            return True
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # GET, HEAD, OPTIONS 요청의 경우 허용
            return True

        if request.user.is_authenticated and request.COOKIES.get('refresh_token') and request.user.is_master:
            if hasattr(obj.master.user, 'email'):
                return obj.master.user.email == request.user.email
            else:
                return False

        return False
