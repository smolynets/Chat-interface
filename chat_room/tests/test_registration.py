"""
Tests.

Test for registration.
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationTest(APITestCase):
    """
    This test checks regostration.

    This test checks next scenarios:
        1. Successful registration.
    """

    def test_registration(self):
        """
        Check registration.

        Successful registration.
        """
        users_count = User.objects.count()
        post_data = {"username": "test_user", "email": "test@email.com",
                     "password": "T12r4567"}
        response = self.client.post(reverse("register_user"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users_count + 1, User.objects.count())
        user = User.objects.last()
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.username, "test_user")
