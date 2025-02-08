# Create your views here.
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

from .views import UserProfileView, StockMatchView, StockView, StockPriceView



router = DefaultRouter()
router.register('userprofile', UserProfileView)
router.register('matches', StockMatchView)
router.register('stock',StockView)
router.register('StockPrice', StockPriceView)

urlpatterns = [
    re_path('^', include(router.urls)),
]
