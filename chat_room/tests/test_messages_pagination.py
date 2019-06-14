"""
Tests for messages.
"""

from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status

from ..models import Message
from .factories import MessageFactory
from .test_base import APITestBaseClass


class MessageTest(APITestBaseClass):
    """
    This test checks messages.

    This test checks next scenarios:
        1. Successful got 10 message as default pagination.
        2. Successful got 1 message with parameter 1.
        3. Failed got 12 message with parameter 12.
    """

    def _build_url(self, params, url):
        url_params = urlencode(params, True)
        return f"{url}?{url_params}"

    def test_messages_default_pagination(self):
        """
        Successful got 10 message as default pagination.
        """
        MessageFactory.create_batch(12)

        response = self.client.get(reverse("message-list"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Message.objects.all().count())
        self.assertEqual(Message.objects.all().count(), 12)
        self.assertEqual(len(response.data["results"]), 10)

    def test_messages_pagination_1_element(self):
        """
        Successful got 1 message with parameter 1.
        """
        MessageFactory.create_batch(12)

        get_data = {"page_size": "1"}
        response = self.client.get(self._build_url(
            get_data, reverse("message-list"))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Message.objects.all().count())
        self.assertEqual(Message.objects.all().count(), 12)
        self.assertEqual(len(response.data["results"]), 1)

    def test_messages_pagination_12_element(self):
        """
        Failed got 12 message with parameter 12.
        """
        MessageFactory.create_batch(12)

        get_data = {"page_size": "12"}
        response = self.client.get(self._build_url(
            get_data, reverse("message-list"))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Message.objects.all().count())
        self.assertEqual(Message.objects.all().count(), 12)
        self.assertEqual(len(response.data["results"]), 10)
