from django.urls import path
# URL routing utility for authentication-related endpoints

from .views import Register, Login, Logout, CSRFToken
# Import views responsible for user authentication and session management


urlpatterns = [
    # Endpoint for new user registration
    path("register/", Register.as_view()),

    # Endpoint for user login and session creation
    path("login/", Login.as_view()),

    # Endpoint for terminating authenticated sessions
    path("logout/", Logout.as_view()),

    # Endpoint to retrieve CSRF token for session-authenticated clients
    path("csrf/", CSRFToken.as_view()),
]