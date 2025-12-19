from rest_framework.authentication import BasicAuthentication  # Basic auth for API access
from rest_framework.views import APIView  # Base class for DRF class-based views
from rest_framework.response import Response  # Standard DRF response object
from rest_framework import status  # HTTP status codes
from rest_framework.permissions import AllowAny  # Allows unauthenticated access

from django.contrib.auth import authenticate, login, logout  # Auth helpers
from django.contrib.auth import get_user_model  # Fetch custom User model
from django.utils import timezone  # Timezone-aware datetime
from datetime import timedelta  # Time duration helper

from django_ratelimit.decorators import ratelimit  # Rate limiting decorator
from django.utils.decorators import method_decorator  # Apply decorators to class-based views

from django.views.decorators.csrf import csrf_exempt  # Disable CSRF protection
from django.middleware.csrf import get_token  # Generate CSRF token

from .serializers import RegisterSerializer  # Serializer for user registration


User = get_user_model()  # Get the active User model (custom or default)

# Security configuration
MAX_ATTEMPTS = 5          # Maximum allowed failed login attempts
LOCK_MINUTES = 15         # Account lock duration after max failures


@method_decorator(csrf_exempt, name="dispatch")  # Disable CSRF for entire class
class Register(APIView):
    """
    Handles new user registration.
    CSRF is disabled because this is an API-only endpoint.
    """
    authentication_classes = [BasicAuthentication]  # Basic auth (not required but explicit)
    permission_classes = [AllowAny]                  # Anyone can register

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)  # Bind request data to serializer
        serializer.is_valid(raise_exception=True)            # Validate input or raise error
        serializer.save()                                   # Create new user
        return Response({"message": "Registered"}, status=status.HTTP_201_CREATED)  # Success response


@method_decorator(csrf_exempt, name="dispatch")  # Disable CSRF for login endpoint
class Login(APIView):
    """
    Authenticates user credentials and creates a session.
    Rate-limited to prevent brute-force attacks.
    """
    authentication_classes = [BasicAuthentication]  # Explicit authentication method
    permission_classes = [AllowAny]                  # Login allowed without auth

    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))  # Limit 5 attempts per minute per IP
    def post(self, request):
        username = request.data.get("username")  # Extract username from request
        password = request.data.get("password")  # Extract password from request

        try:
            user = User.objects.get(username=username)  # Fetch user by username
            if user.is_locked():                         # Check if account is locked
                return Response(
                    {"error": "Account locked. Try later."},  # Lock message
                    status=status.HTTP_403_FORBIDDEN
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},  # Username not found
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(username=username, password=password)  # Validate credentials
        if not user:
            user.failed_attempts += 1  # Increment failed attempt counter
            if user.failed_attempts >= MAX_ATTEMPTS:  # Check max attempts
                user.lock_until = timezone.now() + timedelta(minutes=LOCK_MINUTES)  # Lock account
            user.save(update_fields=["failed_attempts", "lock_until"])  # Save only relevant fields
            return Response(
                {"error": "Invalid credentials"},  # Authentication failed
                status=status.HTTP_401_UNAUTHORIZED
            )

        user.reset_lock()            # Reset failed attempts and unlock account
        login(request, user)         # Create authenticated session

        return Response({"message": "Logged in"}, status=status.HTTP_200_OK)  # Login success


@method_decorator(csrf_exempt, name="dispatch")  # Disable CSRF for logout
class Logout(APIView):
    """
    Terminates the authenticated session.
    """
    authentication_classes = [BasicAuthentication]  # Explicit auth configuration
    permission_classes = [AllowAny]                  # Logout allowed without permission check

    def post(self, request):
        logout(request)  # Destroy session
        return Response({"message": "Logged out"}, status=status.HTTP_200_OK)  # Logout success


class CSRFToken(APIView):
    """
    Optional endpoint to fetch CSRF token (useful for browser clients).
    Not required for Postman/API testing.
    """
    permission_classes = [AllowAny]  # Accessible by anyone

    def get(self, request):
        return Response({"csrfToken": get_token(request)})  # Return CSRF token
