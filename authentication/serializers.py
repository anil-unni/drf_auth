from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Customer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = {
            "id": self.user.id,
            "username": self.user.username,
            "email": self.user.email,
        }
        return data


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "email", "password", "phone_number")

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    user = UserRegistrationSerializer()

    class Meta:
        model = Customer
        fields = ("user", "address", "phone_number", "date_of_birth")

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user_serializer = UserRegistrationSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        customer = Customer.objects.create(user=user, **validated_data)
        return customer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "date_joined",
        ) 
