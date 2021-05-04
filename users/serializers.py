from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "first_name",
            "last_name",
            "username",
            "bio",
            "email",
            "role",
        )
        model = User
        extra_kwargs = {"url": {"lookup_field": "username"}}


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class GetTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.UUIDField()
