#!/bin/sh
echo "Waiting for postgres..."
while ! nc -z $DATABASE_HOST $DATABASE_PORT; do
  sleep 0.1
done
echo "PostgreSQL started"
python manage.py migrate
gunicorn --bind 0.0.0.0:8000 sproutai.wsgi:application
