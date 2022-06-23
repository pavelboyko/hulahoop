from django.test import TransactionTestCase
from rest_framework.test import APIClient
from app.models import Project
from app.fixtures import ProjectFactory

# need this because webhooks under test are processed in a celery task
from hulahoop.celery import app
from celery.contrib.testing.worker import start_worker


class Test(TransactionTestCase):
    """
    ./manage.py test app.api.tests.test_webhook.Test --keepdb --verbosity 2
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.celery_worker = start_worker(app, perform_ping_check=False)
        cls.celery_worker.__enter__()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.celery_worker.__exit__(None, None, None)

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_unknown_project(self) -> None:
        Project.objects.all().delete()
        response = APIClient().post("/api/webhook/0/test/", {})
        self.assertEqual(response.status_code, 404)

    def test_webhook(self) -> None:
        project = ProjectFactory.create()
        slug = "dummy_labeling"
        response = APIClient().post(f"/api/webhook/{project.id}/{slug}/", {})
        self.assertEqual(response.status_code, 200)
