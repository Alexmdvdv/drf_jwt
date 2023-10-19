from rest_framework import serializers

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
