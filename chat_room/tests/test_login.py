"""
Tests.

Test for login.
"""

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LoginTest(APITestCase):
    """
    This test checks login processes.

    This test checks next scenarios:
        1. Successful login.
    """

    def test_login_success(self):
        """
        Check login.

        Successful login.
        """
        User.objects.create_user(
            username="test2_user",
            email="test@emil.com",
            password="password"
        )
        post_data = {"username": "test2_user", "password": "password"}
        response = self.client.post(reverse("login"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_correct_data_for_token_refresh(self):
        """
        Check access jwt urls.

        Token_refresh change previous access token.
        """
        User.objects.create_user(
            username="test2_user",
            email="test@emil.com",
            password="password"
        )
        post_data = {"username": "test2_user", "password": "password"}
        response = self.client.post(reverse("login"), post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response)
        correct_refresh = {"refresh": response.data["refresh"]}
        response = self.client.post(reverse("token_refresh"), correct_refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
