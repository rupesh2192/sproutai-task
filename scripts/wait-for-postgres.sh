#!/bin/sh
set -e
. ./.env
while ! docker ps -q -f status=running -f name="$DATABASE_HOST"; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up"
