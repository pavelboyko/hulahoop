from django.test import TestCase
from rest_framework.test import APIRequestFactory
from app.models import Project
from app.fixtures import ProjectFactory
from app.api import webhook


class Test(TestCase):
    """
    ./manage.py test app.api.tests.test_webhook.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_unknown_project(self) -> None:
        Project.objects.all().delete()
        request = APIRequestFactory().post("/api/webhook/0/test/", {})
        response = webhook(request, 0, "test")
        self.assertEqual(response.status_code, 404)

    def test_webhook(self) -> None:
        project = ProjectFactory.create()
        slug = "dummy_labeling"
        request = APIRequestFactory().post(f"/api/capture/{project.id}/{slug}/", {})
        response = webhook(request, project.id, slug)
        self.assertEqual(response.status_code, 200)
