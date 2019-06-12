"""
Urls for chat_room app.

This urls is included in root urls.
"""


from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import MessageViewSet, RegisterUserView

router = DefaultRouter()
router.register(r'message', MessageViewSet, basename='message')

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("register_user/", RegisterUserView.as_view(), name="register_user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
