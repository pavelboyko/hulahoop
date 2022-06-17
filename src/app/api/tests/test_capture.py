from urllib import response
from dateutil import parser
from django.test import TestCase
from requests import request
from rest_framework.test import APIClient
from app.models import Project, Example, Tag
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
        invalid_data = [{}, {"metadata": {}}, {"fingerprint": {}}]
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
            "attachments": [{"url": "http://example.com", "type": "image"}],
            "metadata": {"a": "b"},
            "predictions": {
                "label": "xxx",
                "score": "0.99",
                "choices": ["xxx", "yyy", "zzz"],
            },
            "annotations": {
                "label": "yyy",
                "choices": ["xxx", "yyy", "zzz"],
            },
            "fingerprint": "xxx",
        }
        response = APIClient().post(path, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example: Example = Example.objects.first()  # type: ignore
        self.assertEqual(example.project, project)
        # self.assertEqual(example.media_url, data["media_url"])
        self.assertDictEqual(example.matadata, data["metadata"])
        self.assertDictEqual(example.predictions, data["predictions"])
        self.assertEqual(example.fingerprint, data["fingerprint"])

    def test_tags(self):
        Example.objects.all().delete()
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        tags = {"a": "b", "c": 1.0}
        data = {
            "media_url": "http://example.com",
            "tags": tags,
        }
        response = APIClient().post(path, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example = Example.objects.first()
        self.assertEqual(Tag.objects.count(), 2)
        for et in Tag.objects.all():
            self.assertEqual(et.example, example)
            self.assertIn(et.key, tags)
            self.assertEqual(et.value, str(tags[et.key]))

    def test_tags_long(self):
        Example.objects.all().delete()
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        tags = {"a" * 100: "b" * 500}
        data = {
            # "media_url": "http://example.com",
            "tags": tags,
        }
        response = APIClient().post(path, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.objects.count(), 1)
        et: Tag = Tag.objects.first()  # type: ignore
        self.assertEqual(et.key, "a" * 32)
        self.assertEqual(et.value, "b" * 255)

    def test_timestamp(self):
        Example.objects.all().delete()
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        data = {"media_url": "http://example.com", "timestamp": "2011-05-02T17:41:36Z"}
        response = APIClient().post(path, data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example: Example = Example.objects.first()  # type: ignore
        self.assertEqual(example.created_at, parser.parse(data["timestamp"]))
