from django.urls import path, include
from rest_framework.routers import DefaultRouter

from contentshub.views import MasterViewSet, KlassViewSet

master_router = DefaultRouter(trailing_slash=False)
master_router.register('masters', MasterViewSet)
klass_router = DefaultRouter(trailing_slash=False)
klass_router.register('klasses', KlassViewSet)

urlpatterns = [
    path('', include(master_router.urls)),
    path('', include(klass_router.urls)),
]
