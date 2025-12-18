from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers
from core.password_utils import get_password_errors

# Retrieve the active User model (supports custom user models)
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    # Explicitly define password field to control validation and write behavior
    password = serializers.CharField(write_only=True)

    class Meta:
        # Bind serializer to User model for registration
        model = User
        fields = ("username", "password")

    def validate_password(self, value):
        # Apply custom password rules to enforce strong passwords at registration
        errors = get_password_errors(value)
        if errors:
            raise serializers.ValidationError(errors)
        return value

    def create(self, validated_data):
        # Extract password to handle hashing and validation manually
        password = validated_data.pop("password")

        # Enforce Django's built-in password validation rules
        try:
            validate_password(password)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})

        # Create user instance without storing raw password
        user = User(**validated_data)

        # Hash password before saving to ensure secure storage
        user.set_password(password)
        user.save()

        return user