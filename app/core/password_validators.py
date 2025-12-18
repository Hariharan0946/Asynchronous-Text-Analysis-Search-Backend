import re
# Regular expressions used to validate password complexity rules

from django.core.exceptions import ValidationError
# Standard Django exception for validation failures


class StrongPasswordValidator:
    """
    Custom password validator to enforce strong password policies.
    This validator is plugged into Django's authentication system
    via AUTH_PASSWORD_VALIDATORS in settings.py.
    """

    def validate(self, password, user=None):
        # Enforce presence of at least one uppercase character
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain an uppercase letter.")

        # Enforce presence of at least one lowercase character
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain a lowercase letter.")

        # Enforce presence of at least one numeric digit
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain a number.")

        # Enforce presence of at least one special character
        if not re.search(r"[!@#$%^&*()_+=\-]", password):
            raise ValidationError("Password must contain a special character.")

    def get_help_text(self):
        # Human-readable explanation of password requirements
        # surfaced in forms or API validation messages
        return "Password must contain uppercase, lowercase, number, and special character."