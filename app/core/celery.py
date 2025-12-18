import os
# Used to access environment variables for configuration

from celery import Celery
# Celery application class for background task processing

# Ensure Django settings are loaded before initializing Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Create Celery application instance scoped to this Django project
app = Celery("core")

# Explicitly configure the message broker to avoid implicit or misconfigured defaults
# Using Redis as broker ensures reliable async task queuing
app.conf.broker_url = os.environ.get(
    "CELERY_BROKER_URL", "redis://redis:6379/0"
)

# Configure result backend to store task execution results (optional but explicit)
# Keeps task state centralized in Redis
app.conf.result_backend = os.environ.get(
    "CELERY_RESULT_BACKEND", "redis://redis:6379/0"
)

# Automatically discover tasks from all installed Django apps
# Allows task definitions to live alongside application logic
app.autodiscover_tasks()