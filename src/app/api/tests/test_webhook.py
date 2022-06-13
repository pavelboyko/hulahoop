from django.test import TestCase
from rest_framework.test import APIClient
from app.models import Project
from app.fixtures import ProjectFactory


class Test(TestCase):
    """
    ./manage.py test app.api.tests.test_webhook.Test --keepdb --verbosity 2
    """

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
