from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


def get_password_errors(password, user=None):
    """
    Helper function to validate passwords and return validation
    errors as a list instead of raising exceptions.

    This is useful for serializers and APIs where we want to
    return structured error responses to the client.
    """
    # Use Django's built-in password validation framework
    # to enforce configured password rules
    try:
        validate_password(password, user)
    except ValidationError as e:
        # Convert validation exceptions into a list of messages
        # suitable for API responses
        return e.messages

    # Return empty list when password passes all validation checks
    return []