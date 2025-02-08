# Create your views here.
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import InvestmentView



router = DefaultRouter()
router.register('investments', InvestmentView)

urlpatterns = [
    re_path('^', include(router.urls)),
]
