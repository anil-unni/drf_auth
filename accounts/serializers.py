from typing import Dict, Any
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile, Role

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.

    This serializer is used for representing user data,
    including id, email, first name, last name, role, and date joined.
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role"]


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.

    This serializer handles the creation of new users,
    requiring an email, first name, last name, and password.
    The password is write-only.
    """

    password: serializers.CharField = serializers.CharField(
        write_only=True, min_length=8
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]

    def create(self, validated_data: Dict[str, Any]) -> User:
        """
        Create a new user with the validated data.

        Parameters:
        - validated_data: A dictionary of validated data for user creation.

        Returns:
        - User: The newly created user instance.
        """
        user: User = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            password=validated_data["password"],
        )
        return user


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    This serializer is used for representing user profile data,
    including date of birth, profile picture, and contact number.
    """

    class Meta:
        model = Profile
        fields = ["date_of_birth", "profile_picture", "contact_number"]


class RoleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Role model.

    This serializer is used for representing role data,
    including id, name, and description.
    """

    class Meta:
        model = Role
        fields = ["id", "name", "description"]
