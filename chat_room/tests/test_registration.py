"""
Test for registration.
"""

from django.urls import reverse
from rest_framework import status

from ..models import User
from .test_base import APITestBaseClass


class RegistrationTest(APITestBaseClass):
    """
    This test checks registration.

    This test checks next scenarios:
        1. Successful registration.
        2. Failed registration without username.
        3. Failed registration without email.
        4. Failed registration without password.
    """

    def test_registration(self):
        """
        Successful registration.
        """
        users_count = User.objects.count()
        post_data = {"username": "register_user", "email": "test@email.com",
                     "password": "T12r4567"}
        response = self.client.post(reverse("register_user"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(users_count + 1, User.objects.count())
        user = User.objects.last()
        self.assertEqual(user.email, "test@email.com")
        self.assertEqual(user.username, "register_user")

    def test_registration_no_username(self):
        """
        Failed registration without username.
        """
        users_count = User.objects.count()
        post_data = {"username": "", "email": "test@email.com",
                     "password": "T12r4567"}
        response = self.client.post(reverse("register_user"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_count, User.objects.count())

    def test_registration_no_email(self):
        """
        Failed registration without email.
        """
        users_count = User.objects.count()
        post_data = {"username": "register_user", "email": "",
                     "password": "T12r4567"}
        response = self.client.post(reverse("register_user"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_count, User.objects.count())

    def test_registration_no_password(self):
        """
        Failed registration without password.
        """
        users_count = User.objects.count()
        post_data = {"username": "register_user", "email": "test@email.com",
                     "password": ""}
        response = self.client.post(reverse("register_user"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(users_count, User.objects.count())
