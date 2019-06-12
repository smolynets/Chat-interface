"""
Views of chat_room.

This file contains views for the chat_room application.
"""

from rest_framework.generics import CreateAPIView
from .serializers import UserCreateSerializer


class RegisterUserView(CreateAPIView):
    """
    Create user view.

    This view provide UserCreateSerializer.

    """

    serializer_class = UserCreateSerializer
