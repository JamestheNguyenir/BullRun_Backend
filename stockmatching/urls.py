# Create your views here.
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import UserProfileView



router = DefaultRouter()
router.register('UserProfile', UserProfileView)

urlpatterns = [
    re_path('^', include(router.urls)),
]
