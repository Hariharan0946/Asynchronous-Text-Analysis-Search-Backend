from pathlib import Path
# Path utility for building platform-independent file paths

# Base directory of the project (used for resolving paths consistently)
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key used by Django for cryptographic signing (development value)
SECRET_KEY = "dev-secret"

# Enable debug mode for development and easier troubleshooting
DEBUG = True

# Allow all hosts in development and containerized environments
ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    # Core Django applications required for authentication, sessions, and admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party apps for building REST APIs and handling CORS
    "rest_framework",
    "corsheaders",

    # Project-specific applications
    "auth_app",
    "text_app",
]


MIDDLEWARE = [
    # Enable CORS handling for API requests from different origins
    "corsheaders.middleware.CorsMiddleware",

    # Standard Django security and request/response middleware
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",

    # CSRF protection middleware for session-based authentication
    "django.middleware.csrf.CsrfViewMiddleware",

    # Authentication and messaging middleware
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",

    # Clickjacking protection
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# Root URL configuration for the project
ROOT_URLCONF = "core.urls"

# WSGI entry point for serving the application
WSGI_APPLICATION = "core.wsgi.application"


TEMPLATES = [
    {
        # Django template backend configuration
        "BACKEND": "django.template.backends.django.DjangoTemplates",

        # No custom template directories required for API-only backend
        "DIRS": [],

        # Enable app-level template discovery
        "APP_DIRS": True,

        "OPTIONS": {
            # Context processors required for authentication and debugging
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


DATABASES = {
    "default": {
        # PostgreSQL database configuration for persistent storage
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "codemonk",
        "USER": "codemonk",
        "PASSWORD": "codemonk",

        # Database service hostname defined in docker-compose
        "HOST": "db",
        "PORT": 5432,
    }
}

# Specify custom user model for authentication
AUTH_USER_MODEL = "auth_app.User"


# Static files configuration (minimal since no frontend is served)
STATIC_URL = "/static/"

# Default primary key field type for new models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Allow cross-origin API requests (useful for API testing tools and clients)
CORS_ALLOW_ALL_ORIGINS = True