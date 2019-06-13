"""
Factories for chat_room app.
"""

import factory
from ..models import Message, Room, User


class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory class.

    This class create news by factory_boy application.

    """

    class Meta:
        """
        Meta class.

        Defenition meta data for UserFactory class.

        """

        model = User

    username = factory.Faker("name")
    first_name = factory.Faker("name")
    last_name = factory.Faker("name")
    email = factory.Faker("email")


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Room

    name = factory.Faker("sentence")


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    text = factory.Faker("sentence")
    room = factory.SubFactory(RoomFactory)
    author = factory.SubFactory(UserFactory)
