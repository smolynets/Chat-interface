from django.contrib.auth import password_validation
from .models import Comment, Message, User
from django.core import exceptions
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.utils.translation import gettext as _


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Create of user.

    This class provide creation of user with three fields: username, email
    and password.
    """

    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
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


class CommentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class MessageModelSerializer(serializers.ModelSerializer):
    """
    MessageModelSerializer class.
    """

    comments = CommentModelSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Message
        fields = ("id", "text", "room", "author", "comments")

    def create(self, validated_data):
        """
        Create Message instance with current logged user.
        """

        validated_data["author"] = self.context["request"].user
        if "comments" in validated_data:
            comments_data = validated_data.pop("comments")
            message = Message.objects.create(**validated_data)
            for comment_data in comments_data:
                Comment.objects.create(message=message, **comment_data)
        else:
            message = Message.objects.create(**validated_data)
        return message

    def update(self, instance, validated_data):
        """
        Only authenticated user and author can update message.
        """

        if self.context["request"].method.upper() in ["PUT", "PATCH"]:
            if not self.context["request"].user.is_authenticated:
                raise serializers.ValidationError(
                    _("Only authenticated user can update")
                )
            if self.context["request"].user != instance.author:
                raise serializers.ValidationError(
                    _("Only author of message can update")
                )
        instance.text = validated_data.get("text", instance.text)
        instance.save()
        return instance
