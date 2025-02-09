# Create your views here.
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import UserProfileView, StockView



router = DefaultRouter()
router.register('userprofile', UserProfileView)
router.register('stock',StockView)

urlpatterns = [
    re_path('^', include(router.urls)),
]
