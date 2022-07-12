import os

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "db")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_NAME = os.environ.get("POSTGRES_NAME")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")

HAS_POSTGRES = all(
    [
        POSTGRES_NAME,
        POSTGRES_USER,
        POSTGRES_PASSWORD,
    ]
)

if HAS_POSTGRES:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": POSTGRES_NAME,
            "USER": POSTGRES_USER,
            "PASSWORD": POSTGRES_PASSWORD,
            "HOST": POSTGRES_HOST,
            "PORT": POSTGRES_PORT,
        }
    }
else:
    # this configuration is used for testing
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": "db",
        }
    }
