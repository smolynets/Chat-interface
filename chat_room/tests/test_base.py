"""
This test is inherited by tests of other apps.
"""

from django.urls import reverse

from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.settings import api_settings


class APIRestAuthJWTClient(APIClient):
    """
    APIRestAuthJWTClient class.

    Login with jwt tokens.
    """

    def login(self, login_name="login", **credentials):
        """
        Login method.

        Get tokens, if successful login.
        """
        login_endpoint = reverse(login_name)
        login_response = self.post(login_endpoint, credentials, format="json")
        if login_response.status_code == 200:
            self.credentials(
                HTTP_AUTHORIZATION="{0} {1}".format(
                    api_settings.defaults["AUTH_HEADER_TYPES"][0],
                    login_response.data["access"]
                )
            )
            return True
        else:
            return False


class APITestBaseClass(APITestCase):
    """
    APITestBaseClass class.

    Get APITestBaseClass.
    """

    client_class = APIRestAuthJWTClient
