from .settings import *

SECRET_KEY = "t0p s3cr3t"
ALLOWED_HOSTS = ["*"]
DEBUG = True
DEFAULT_FILE_STORAGE = "utils.storages.file.CommonFileSystemStorage"
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
