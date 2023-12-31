from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True,
    )

    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["nickname", "email", "firstname", "lastname", "password", "refresh_token", "access_token"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(
        min_length=8,
        max_length=128,
        write_only=True
    )

    refresh_token = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError(
                "An email address is required to log in"
            )

        if password is None:
            raise serializers.ValidationError(
                "A password is required to log in"
            )
        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                "A user with this email and password was not found"
            )

        if not user.is_active:
            raise serializers.ValidationError(
                "This user has been deactivated"
            )

        return {
            "email": user.email,
            "refresh_token": user.refresh_token,
            "access_token": user.access_token
        }
