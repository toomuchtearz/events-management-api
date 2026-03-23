from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
            "password",
        )

        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "validators": [validate_password],
            },
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class ManageUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "username",
        )
