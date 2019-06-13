from django.contrib.auth import password_validation
from .models import Message, User
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Create of user.

    This class provide creation of user with three fields: username, email
    and password.
    """

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(validators=[UniqueValidator(
        queryset=User.objects.all())]
    )

    class Meta:
        """
        Meta class.

        This class describe model and fields.
        """

        model = User
        fields = ["username", "email", "password"]

    def validate(self, data):
        """
        Validate password.

        Validate length of password.
        """
        user = User(**data)
        password = data.get("password")
        errors = dict()
        try:
            password_validation.validate_password(password=password, user=user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super(UserCreateSerializer, self).validate(data)

    def create(self, validated_data):
        """
        Create user instance.

        Updates the standard method to hash the password
        """
        user = super(UserCreateSerializer, self).create(validated_data)
        user.set_password(user.password)
        user.save()
        return user


class MessageModelSerializer(serializers.ModelSerializer):
    """
    MessageModelSerializer class.
    """

    class Meta:
        model = Message
        fields = ("id", "text", "room", "author")

    def create(self, validated_data):
        """
        Create Message instance with current logged user.
        """

        validated_data["author"] = self.context["request"].user
        return Message.objects.create(**validated_data)
