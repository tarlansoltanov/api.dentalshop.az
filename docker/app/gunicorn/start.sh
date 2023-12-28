#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

# Using `gunicorn` for production, see:
# http://docs.gunicorn.org/en/stable/configure.html

# Check that $DJANGO_ENV is set to "production"
echo "DJANGO_ENV is $DJANGO_ENV"
if [ "$DJANGO_ENV" != 'prod' ]; then
  echo 'Error: DJANGO_ENV is not set to "prod" (production).'
  echo 'Application will not start.'
  exit 1
fi

export DJANGO_ENV

# Run python specific scripts:
python manage.py collectstatic --noinput

# Start gunicorn
echo "Starting gunicorn..."
gunicorn --config python:docker.app.gunicorn.config server.wsgi
