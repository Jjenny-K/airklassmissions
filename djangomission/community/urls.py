from django.urls import path, include
from rest_framework.routers import DefaultRouter

from community.views import QuestionViewSet

community_router = DefaultRouter(trailing_slash=False)
community_router.register('questions', QuestionViewSet, basename='questions')

urlpatterns = [
    path('', include(community_router.urls)),
]
