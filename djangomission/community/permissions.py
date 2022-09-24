import re

from rest_framework import permissions

from contentshub.models import Klass
from community.models import Question


class QuestionIsOwnerOrReadOnly(permissions.BasePermission):
    """
        인증받은 사용자 본인이 작성한 질문이 아닐 경우 권한 제한
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


class QuestionDestroyIsOwnerIsMaster(permissions.BasePermission):
    """
        인증받은 사용자 본인이 작성한 질문이 아닐 경우, 본인이 등록한 강의의 질문이 아닐 경우 권한 제한
    """

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.COOKIES.get('refresh_token'):
            if hasattr(obj.user, 'email'):
                return (obj.user.email == request.user.email) or (obj.klass.master.user.email == request.user.email)
            else:
                return False

        return False


class AnswerIsMasterOrReadOnly(permissions.BasePermission):
    """
        인증받은 사용자 본인이 등록한 강의가 아닐 경우 권한 제한
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.COOKIES.get('refresh_token') and request.user.is_master:
            klass_list = Klass.objects.filter(master__user_id=request.user.id)
            question = Question.objects.get(id=re.sub(r'[^0-9]', '', request.path))

            if question.klass in klass_list:
                return True
            else:
                return False
        else:
            return False
