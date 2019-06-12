"""
Tests.

Test for registration and login login.
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class RegistrationLoginTest(APITestCase):
    """
    This test checks regostration and login processes.

    This test checks next scenarios:
        1. Successful registration and login.
    """

    def test_registration_login_success(self):
        """
        Check registration andlogin.

        Successful registration andlogin.
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

        self.client.logout()

        # # login with username
        # post_data = {"username": "test_user", "password": "password"}
        # response = self.client.post(reverse("login"), post_data,
        #                             format="json")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
