#!/usr/bin/env sh
set -e

# Production entrypoint (used by the Docker image CMD, e.g. on Render).
# Local docker-compose overrides this with its own runserver command.

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

# Seed the catalog. Set RESEED=1 (env) to wipe & rebuild the catalog from code
# (keeps users); otherwise only seed when the DB is empty.
if [ "$RESEED" = "1" ]; then
    echo "Reseeding catalog (RESEED=1)..."
    python manage.py seed_demo --reseed || true
else
    echo "Seeding catalog (if empty)..."
    python manage.py seed_demo --if-empty || true
fi

PORT="${PORT:-8000}"
echo "Starting gunicorn on :${PORT}..."
exec gunicorn config.wsgi:application \
    --bind "0.0.0.0:${PORT}" \
    --workers "${WEB_CONCURRENCY:-3}" \
    --timeout 120
