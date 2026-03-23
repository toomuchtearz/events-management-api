from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "first_name", "last_name")

        extra_kwargs = {
            "password": {
                "write_only": True,
                "style": {"input_type": "password"},
                "validators": [validate_password],
            },
            "first_name": {"required": True, "allow_blank": False},
            "last_name": {"required": True, "allow_blank": False},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class ManageUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )
        read_only_fields = ("email",)
