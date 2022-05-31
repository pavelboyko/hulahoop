# Starting developing locally

## Prerequisites

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop)
2. Clone the Hulahoop respository. All future commands assume you're inside the root repository folder:
```
git clone https://github.com/pavelboyko/hulahoop.git && cd hulahoop/
```

## Running locally

1. Launch database and app services
```
docker-compose up
```

2. On the first run create a superuser
```
docker exec -it hulahoop_app_1 /opt/hulahoop/manage.py createsuperuser 
```

3. Open http://localhost:8000 to see the app. Use login and password from the previous step to login.

## Changing code locally

There is no need to rebuild or restart the app container if you only change code, since the code is mounted directly to the container. 

If requirements change (e.g. you're using new `pip` or system package) you have to rebuild and restart the app:
```
docker-compose down
docker-compose build
docker-compose up
```

If database models change you have to create and apply migrations:

```
docker exec -it hulahoop_app_1 /opt/hulahoop/manage.py makemigrations
docker exec -it hulahoop_app_1 /opt/hulahoop/manage.py migrate
```

## What's inside Hulahoop

Services:
- db: the PostgreSQL database
- app: the Django app

### Inside the app container

The app is located in `/opt/hulahoop`.

The following environment variables are defined in the `app` container:

- POSTGRES_NAME: database name
- POSTGRES_USER: database user
- POSTGRES_PASSWORD: database password

### Inside the database container

Hulahoop uses PostgreSQL 14 as a transactional database. When running locally the database is launched in a separate container named `docker_compose_db_1`.
If you need direct access to the database, use the following credentials:

```
POSTGRES_DB=hulahoop
POSTGRES_USER=hulahoop
POSTGRES_PASSWORD=hulahoop
```

## Source code structure
- `docs` -- Keep this up to date, please.
- `src`
  - `app` -- Backend sources
  - `hulahoop` -- Django configuration
  - `mpa` -- Multi-Page App frontend (to be replaced by and SPA frontend at some point I guess)
  - `entrypoint-dev.sh` -- dev server launch script
  - `manage.py` -- Django swiss army knife
- `docker-compose.yml` -- service launch instructions
- `Dockerfile` -- app container build instructions. Update this file when you add new system dependencies.
- `requirements.txt` -- Python requirements. Update this file when you add new `pip` packages.



