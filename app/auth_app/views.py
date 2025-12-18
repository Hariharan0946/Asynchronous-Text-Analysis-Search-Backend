from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from django_ratelimit.decorators import ratelimit
from django.utils.decorators import method_decorator

from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

from .serializers import RegisterSerializer


User = get_user_model()

# Security configuration
MAX_ATTEMPTS = 5
LOCK_MINUTES = 15


@method_decorator(csrf_exempt, name="dispatch")
class Register(APIView):
    """
    Handles new user registration.
    CSRF is disabled because this is an API-only endpoint.
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Registered"}, status=status.HTTP_201_CREATED)


@method_decorator(csrf_exempt, name="dispatch")
class Login(APIView):
    """
    Authenticates user credentials and creates a session.
    Rate-limited to prevent brute-force attacks.
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    @method_decorator(ratelimit(key="ip", rate="5/m", block=True))
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        try:
            user = User.objects.get(username=username)
            if user.is_locked():
                return Response(
                    {"error": "Account locked. Try later."},
                    status=status.HTTP_403_FORBIDDEN
                )
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = authenticate(username=username, password=password)
        if not user:
            user.failed_attempts += 1
            if user.failed_attempts >= MAX_ATTEMPTS:
                user.lock_until = timezone.now() + timedelta(minutes=LOCK_MINUTES)
            user.save(update_fields=["failed_attempts", "lock_until"])
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user.reset_lock()
        login(request, user)

        return Response({"message": "Logged in"}, status=status.HTTP_200_OK)


@method_decorator(csrf_exempt, name="dispatch")
class Logout(APIView):
    """
    Terminates the authenticated session.
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"}, status=status.HTTP_200_OK)


class CSRFToken(APIView):
    """
    Optional endpoint to fetch CSRF token (useful for browser clients).
    Not required for Postman/API testing.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({"csrfToken": get_token(request)})