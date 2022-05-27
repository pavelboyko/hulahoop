#!/bin/sh
# adapted from https://docs.docker.com/compose/startup-order/
set -e

host="db"
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -d "$POSTGRES_NAME" -U "$POSTGRES_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 5
done

>&2 echo "Postgres is up - starting service"

python manage.py makemigrations --noinput && \
python manage.py migrate --noinput && \
python manage.py runserver 0.0.0.0:8000