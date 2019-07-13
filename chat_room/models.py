"""
Models for chat_room app.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext as _


class User(AbstractUser):
    """
    Set User model.

    This model is inherited from default user model.
    """

    last_message = models.DateTimeField(
        _("last message"), default=None, blank=True, null=True
    )

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
        verbose_name=_("Room"), null=True, to="chat_room.Room", on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        verbose_name=_("author"),
        to="chat_room.User",
        null=True,
        related_name="author",
        on_delete=models.CASCADE,
    )
    created = models.DateTimeField(_("Created"), default=timezone.now)

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    """
    Set Comment model.
    """

    text = models.CharField(max_length=255, default="")
    message = models.ForeignKey(
        verbose_name=_("Message"),
        related_name="comments",
        null=True,
        to="chat_room.Message",
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ["-id"]
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return str(self.id)


@receiver(post_save, sender=Message)
def post_save_handler(sender, instance, created, **kwargs):
    """
    Post save handler.

    Changing of last_message of related User.
    """

    if instance.author:
        user = User.objects.get(id=instance.author.id)
        user.last_message = timezone.now()
        user.save(update_fields=["last_message"])
