from urllib import response
from django.test import TestCase
from requests import request
from rest_framework.test import APIClient
from app.models import Project, Example
from app.fixtures import ProjectFactory


class Test(TestCase):
    """
    ./manage.py test app.api.tests.test_capture.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_unknown_project(self) -> None:
        Project.objects.all().delete()
        response = APIClient().post("/api/capture/0/", {})
        self.assertEqual(response.status_code, 404)

    def test_invalid_request(self) -> None:
        invalid_data = [{}, {"media_url": {}}, {"properties": {}}, {"fingerprint": {}}]
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"

        for data in invalid_data:
            response = APIClient().post(path, data, format="json")
            self.assertEqual(response.status_code, 400)

    def test_create_example(self) -> None:
        Example.objects.all().delete()

        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        data = {
            "media_url": "http://example.com",
            "properties": {"a": "b"},
            "fingerprint": "xxx",
        }
        response = APIClient().post(path, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example = Example.objects.first()
        self.assertEqual(example.project, project)
        self.assertEqual(example.media_url, data["media_url"])
        self.assertDictEqual(example.properties, data["properties"])
        self.assertEqual(example.fingerprint, data["fingerprint"])
