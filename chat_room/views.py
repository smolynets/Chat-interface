"""
Views of chat_room.

This file contains views for the chat_room application.
"""

from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from .serializers import MessageModelSerializer, UserCreateSerializer
from .models import User


class RegisterUserView(CreateAPIView):
    """
    Create user view.

    This view provide UserCreateSerializer.

    """

    serializer_class = UserCreateSerializer


class MessageViewSet(ModelViewSet):
    """
    A viewset for viewing and editing message instances.
    """
    serializer_class = MessageModelSerializer
    queryset = User.objects.all()
