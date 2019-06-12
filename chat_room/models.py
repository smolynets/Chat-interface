"""
Models for chat_room app.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class User(AbstractUser):
    """
    Set User model.

    This model is inherited from default user model.
    """

    pass

    class Meta:
        ordering = ["date_joined"]
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        return self.username


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

    text = models.CharField(max_length=255, default="")
    room = models.ForeignKey(
        verbose_name=_("Room"), null=True, to="chat_room.Room",
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(verbose_name=_("author"), to="chat_room.User",
                               null=True, related_name='author',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return self.id
