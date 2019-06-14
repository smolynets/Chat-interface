"""
Tests for messages.
"""

from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from .test_base import APITestBaseClass

from ..models import Message, Room
from .factories import MessageFactory


class MessageTest(APITestBaseClass):
    """
    This test checks messages.

    This test checks next scenarios:
        1. Successful create message by post method with current user
        2. Failed creation without post data.
        3. Successful got list by get method.
        4. Successful changed message by put method.
        5. Successful changed message by patch method.
        6. Can't  get messages older 30 minutes.
    """

    def test_post_message(self):
        """
        Successful create message by post method with current user.
        """

        self.assertTrue(self.client.login(username=self.user.username,
                        password="password"))

        room = Room.objects.create(name="test_room")

        post_data = {
            "text": "test_text",
            "room": room.id
        }
        Messages_count_before = Message.objects.count()
        response = self.client.post(reverse("message-list"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["text"], "test_text")
        self.assertEqual(response.data["room"], room.id)
        self.assertEqual(response.data["author"], self.user.id)
        self.assertEqual(Message.objects.count(), Messages_count_before + 1)
        self.assertFalse(self.user.last_message)
        self.user.refresh_from_db()
        self.assertEqual(self.user.last_message.strftime("%m/%d/%Y, %H:%M"),
                         timezone.now().strftime("%m/%d/%Y, %H:%M"))

    def test_post_message_without_data(self):
        """
        Failed creation without post data.
        """

        post_data = {
            "text": "",
            "room": None,
            "author": None
        }
        Messages_count_before = Message.objects.count()
        response = self.client.post(reverse("message-list"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Message.objects.count(), Messages_count_before)

    def test_get_message(self):
        """
        Successful got list by get method.
        """

        MessageFactory.create_batch(12)

        response = self.client.get(reverse("message-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 12)
        self.assertEqual(len(response.data["results"]), 10)
        saved_messages = [message.id for message in Message.objects.all()[:10]]
        for message in response.data["results"]:
            self.assertIn(message["id"], saved_messages)

    def test_put_message(self):
        """
        Successful changed message by put method.
        """

        self.assertTrue(self.client.login(username=self.user.username,
                        password="password"))
        message = MessageFactory(text="put_test", author=self.user)
        self.assertEqual(message.text, "put_test")
        response = self.client.put(reverse("message-detail",
                                   args=[message.id]),
                                   {"text": "put_test2"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.text, "put_test2")

    def test_put_message_not_author(self):
        """
        Failed changed message by put method if current user is not author.
        """

        self.assertTrue(self.client.login(username=self.user_two.username,
                        password="password"))
        message = MessageFactory(text="put_test", author=self.user)
        self.assertEqual(message.text, "put_test")
        response = self.client.put(reverse("message-detail",
                                   args=[message.id]),
                                   {"text": "put_test2"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data[0]),
                         "Only author of message can update")
        message.refresh_from_db()
        self.assertEqual(message.text, "put_test")

    def test_patch_message(self):
        """
        Successful changed message by patch method.
        """

        self.assertTrue(self.client.login(username=self.user.username,
                        password="password"))
        message = MessageFactory(text="put_test", author=self.user)
        self.assertEqual(message.text, "put_test")
        response = self.client.patch(reverse("message-detail",
                                     args=[message.id]),
                                     {"text": "put_test2"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        message.refresh_from_db()
        self.assertEqual(message.text, "put_test2")

    def test_patch_message_not_author(self):
        """
        Failed changed message by patch method if current user is not author.
        """

        self.assertTrue(self.client.login(username=self.user_two.username,
                        password="password"))
        message = MessageFactory(text="put_test", author=self.user)
        self.assertEqual(message.text, "put_test")
        response = self.client.patch(reverse("message-detail",
                                     args=[message.id]),
                                     {"text": "put_test2"}, format="json")
        self.assertEqual(str(response.data[0]),
                         "Only author of message can update")
        message.refresh_from_db()
        self.assertEqual(message.text, "put_test")

    def test_age_message(self):
        """
        Can't get messages older 30 minutes.
        """

        message = MessageFactory(text="put_test", created=(
            timezone.now() - timedelta(minutes=30))
        )
        self.assertEqual(message.text, "put_test")

        response = self.client.put(reverse("message-detail",
                                   args=[message.id]),
                                   {"text": "put_test2"}, format="json")                    
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        message.refresh_from_db()
        self.assertEqual(message.text, "put_test")

        response = self.client.patch(reverse("message-detail",
                                     args=[message.id]),
                                     {"text": "put_test2"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        message.refresh_from_db()
        self.assertEqual(message.text, "put_test")
