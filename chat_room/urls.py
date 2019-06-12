"""
Urls for chat_room app.

This urls is included in root urls.
"""


from django.urls import path

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView, TokenRefreshView
# )

from .views import RegisterUserView

urlpatterns = [
    # path("login/", LoginUserView.as_view(), name="login"),
    path("register_user/", RegisterUserView.as_view(), name="register_user"),
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
