#!/usr/bin/env sh
set -e

# Production entrypoint (used by the Docker image CMD, e.g. on Render).
# Local docker-compose overrides this with its own runserver command.

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Seed demo data only if the database is empty (safe to run every deploy).
echo "Seeding demo data (if empty)..."
python manage.py seed_demo --if-empty || true

PORT="${PORT:-8000}"
echo "Starting gunicorn on :${PORT}..."
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT}" \
    --workers "${WEB_CONCURRENCY:-3}" \
    --timeout 120
