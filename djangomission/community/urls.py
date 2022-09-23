from django.urls import path, include
from rest_framework.routers import DefaultRouter

from community.views import QuestionViewSet

question_router = DefaultRouter(trailing_slash=False)
question_router.register('questions', QuestionViewSet)

urlpatterns = [
    path('', include(question_router.urls)),
]
