from django.urls import path, include
from rest_framework.routers import DefaultRouter

from contentshub.views import MasterViewSet, KlassViewSet

contentshub_router = DefaultRouter(trailing_slash=False)
contentshub_router.register('masters', MasterViewSet)
contentshub_router.register('klasses', KlassViewSet)

urlpatterns = [
    path('', include(contentshub_router.urls)),
]
