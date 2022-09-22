from django.urls import path, include
from rest_framework.routers import DefaultRouter

from contentshub.views import MasterViewSet

master_router = DefaultRouter(trailing_slash=False)
master_router.register('masters', MasterViewSet)

urlpatterns = [
    path('', include(master_router.urls)),
]
