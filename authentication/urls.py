# Create your views here.
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from authentication.views import RegisterView, LogoutAPIView, LoginAPIView, UserViewSet

router = DefaultRouter()
router.register('user', UserViewSet)

urlpatterns = [
    path('register/', RegisterView.as_view(), name="register"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutAPIView.as_view(), name="logout"),
    re_path('^', include(router.urls)),
]
