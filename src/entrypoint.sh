#!/bin/sh
set -e

# wait until Postgres is ready
SQL_HOST="db"
SQL_PORT=5432
while ! nc -z $SQL_HOST $SQL_PORT; do
  echo "Postgres is unavailable - sleeping"
  sleep 5
done

# we don't wait for Redis here because it starts faster than Postgres
# though we should in principle wait for both to start before starting the app
echo "Postgres is up - starting service"

# Obtain an exclusive lock for preparation to prevent parallel installs and migrations
prepare() {
  python manage.py migrate --noinput && \
  python manage.py collectstatic --noinput
}

(
   flock -e 9
   prepare
) 9>> /var/lock/hulahoop.entrypoint.lock

exec "$@"
