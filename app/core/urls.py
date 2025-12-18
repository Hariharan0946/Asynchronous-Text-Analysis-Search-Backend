from django.urls import path, include
# URL utilities for composing application-level routes


urlpatterns = [
    # Namespace for all authentication-related APIs
    path("api/auth/", include("auth_app.urls")),

    # Namespace for text processing and search APIs
    path("api/text/", include("text_app.urls")),
]