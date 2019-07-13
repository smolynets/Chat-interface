"""
Views of chat_room.

This file contains views for the chat_room application.
"""

from django.utils import timezone
from datetime import timedelta
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import ModelViewSet

from .models import Message
from .pagination import MessagesPagination
from .serializers import MessageModelSerializer, UserCreateSerializer


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
    pagination_class = MessagesPagination

    def get_queryset(self):
        """
        Get queryset method of ChaptersModelViewSet.

        This method reports messages that are not older than 30 minutes
        in PUT and Patch methods.
        """
        if self.action in ["update", "partial_update"]:
            return Message.objects.filter(
                created__gt=(timezone.now() - timedelta(minutes=30))
            )
        return Message.objects.all()
