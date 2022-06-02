from celery import Celery
from django.conf import settings

app = Celery("hulahoop_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.task_default_queue = "celery"
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS + ["app.tasks"])

