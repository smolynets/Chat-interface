"""
Models for chat_room app.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class Room(models.Model):
    """
    Set Room model.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    def __str__(self):
        return self.name


class Message(models.Model):
    """
    Set message model.
    """

    room = models.ForeignKey(
        verbose_name=_("Message"), to="chat_room.Room",
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.id
