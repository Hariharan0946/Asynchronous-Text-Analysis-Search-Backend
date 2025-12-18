FROM python:3.11-slim
# Lightweight Python base image suitable for production containers

WORKDIR /app
# Set working directory for application code

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    netcat-openbsd \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*
# Install system dependencies:
# - gcc: required for building Python packages with native extensions
# - postgresql-client: enables database connectivity and health checks
# - netcat-openbsd: useful for service readiness checks in entrypoint
# - dos2unix: normalize script line endings for Linux containers

COPY requirements.txt .
# Copy dependency definitions separately to leverage Docker layer caching

RUN pip install --no-cache-dir -r requirements.txt
# Install Python dependencies without caching to reduce image size

COPY app /app
# Copy application source code into container

COPY entrypoint.sh /entrypoint.sh
# Copy entrypoint script responsible for startup orchestration

RUN dos2unix /entrypoint.sh && chmod +x /entrypoint.sh
# Ensure entrypoint script has correct line endings and execute permission

ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
# Execute entrypoint script before running the main process

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]
# Start Django application using Gunicorn WSGI server