"""
Override login backends.

All custom auth backends must be here.
"""

from django.contrib.auth import get_user_model

User = get_user_model()


class CustomModelBackend(object):
    """
    Change UsernameModelBackend.

    Login via email.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate method.

        Change login to email instead username.
        """

        user = User.objects.get(username=username)
        if user.check_password(password):
            return user

    def get_user(self, user_id):
        """
        Get_user method.

        Get user by user_id.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
