"""
Tests.

Test for login.
"""

from django.urls import reverse
from rest_framework import status

from ..models import User
from .test_base import APITestBaseClass


class LoginTest(APITestBaseClass):
    """
    This test checks login processes.

    This test checks next scenarios:
        1. Successful login.
        2. Failed login with wrong username.
        3. Failed login with wrong password.
        4. Token_refresh change previous access token
    """

    def setUp(self):
        """
        Creeate User.
        """
        self.user = User.objects.create_user(
            username="test_user",
            email="test@emil.com",
            password="password"
        )

    def test_login_success(self):
        """
        Successful login.
        """

        post_data = {"username": "test_user", "password": "password"}
        response = self.client.post(reverse("login"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_wrong_username(self):
        """
        Failed login with wrong username.
        """

        post_data = {"username": "wrong_username", "password": "password"}
        response = self.client.post(reverse("login"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_password(self):
        """
        Failed login with wrong password.
        """

        post_data = {"username": "test_user", "password": "wrong_password"}
        response = self.client.post(reverse("login"), post_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_correct_data_for_token_refresh(self):
        """
        Token_refresh change previous access token.
        """

        post_data = {"username": "test_user", "password": "password"}
        response = self.client.post(reverse("login"), post_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response)
        correct_refresh = {"refresh": response.data["refresh"]}
        response = self.client.post(reverse("token_refresh"), correct_refresh)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
