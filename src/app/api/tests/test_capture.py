from urllib import response
from django.test import TestCase
from requests import request
from rest_framework.test import APIRequestFactory
from app.models import Project, Example
from app.fixtures import ProjectFactory
from app.api.capture import capture


class Test(TestCase):
    """
    ./manage.py test app.api.tests.test_capture.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_unknown_project(self) -> None:
        Project.objects.all().delete()
        request = APIRequestFactory().post("/api/capture/0/", {})
        response = capture(request, 0)
        self.assertEqual(response.status_code, 404)

    def test_invalid_request(self) -> None:
        invalid_data = [
            {},
            {"media_url": {}},
            {"properties": {}},
        ]
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"

        for data in invalid_data:
            request = APIRequestFactory().post(path, data, format="json")
            response = capture(request, project.id)
            self.assertEqual(response.status_code, 400)

    def test_create_example(self) -> None:
        Example.objects.all().delete()

        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        data = {"media_url": "http://example.com", "properties": {"a": "b"}}
        request = APIRequestFactory().post(path, data, format="json")
        response = capture(request, project.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example = Example.objects.first()
        self.assertEqual(example.project, project)
        self.assertEqual(example.media_url, data["media_url"])
        self.assertDictEqual(example.properties, data["properties"])
