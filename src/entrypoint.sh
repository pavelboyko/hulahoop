#!/bin/sh
set -e

# wait until Postgres is ready
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "Postgres is unavailable - sleeping"
  sleep 5
done

# We don't wait for Redis here because it starts faster than Postgres
# though we should in principle wait for both to start before starting the app
echo "Postgres is up - starting service"

# We use a file-based lock to prevent parallel migrations for now
# To make this work we have a shared /var/lock/ volume across app and celery workers containers
# This must be somehow reworked for cluster deployment 
prepare() {
  python manage.py migrate --noinput && \
  python manage.py collectstatic --noinput
}

(
   flock -e 9
   prepare
) 9>> /var/lock/hulahoop.entrypoint.lock

exec "$@"
