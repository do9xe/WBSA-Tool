#!/usr/bin/env sh
set -e

# Ensure we're in the app directory
cd /code/WBSAtool

# Collect static files at container startup (works with a mounted /static volume)
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Execute the CMD passed to the container
exec "$@"
