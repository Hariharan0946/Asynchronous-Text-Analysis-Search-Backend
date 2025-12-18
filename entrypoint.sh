#!/bin/bash
set -e

echo " Starting Codemonk Backend"

echo "Waiting for PostgreSQL..."
until nc -z db 5432; do sleep 2; done
echo "PostgreSQL ready"

echo " Waiting for Redis..."
until nc -z redis 6379; do sleep 2; done
echo " Redis ready"

echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

echo "Creating superuser (if not exists)..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='admin').exists() or \
User.objects.create_superuser('admin','admin@codemonk.com','Admin@1234')
"

echo "Starting server"
exec "$@"