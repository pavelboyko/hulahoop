from urllib import response
from dateutil import parser
from django.test import TestCase
from requests import request
from rest_framework.test import APIClient
from app.models import Project, Example, Tag, Attachment
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
        invalid_data = [{}]
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"

        for data in invalid_data:
            response = APIClient().post(path, data, format="json")
            print(response.json())
            self.assertEqual(response.status_code, 400)

    def test_create_example(self) -> None:
        Example.objects.all().delete()

        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        data = {
            "attachments": [{"url": "http://example.com"}],
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
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example: Example = Example.objects.first()  # type: ignore
        self.assertEqual(example.project, project)
        self.assertDictEqual(example.metadata, data["metadata"])
        self.assertDictEqual(example.predictions, data["predictions"])
        self.assertDictEqual(example.annotations, data["annotations"])
        self.assertEqual(example.fingerprint, data["fingerprint"])

        attachments = example.attachment_set.all()  # type: ignore
        self.assertEqual(attachments.count(), 1)
        self.assertEqual(attachments.first().example, example)
        self.assertEqual(attachments.first().url, data["attachments"][0]["url"])
        self.assertEqual(attachments.first().type, Attachment.Type.unknown)

    def test_tags(self) -> None:
        Example.objects.all().delete()
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        tags = {"a": "b", "c": 1.0}
        data = {
            "tags": tags,
            "attachments": [{"url": "xxx"}],
        }
        response = APIClient().post(path, data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example = Example.objects.first()
        self.assertEqual(Tag.objects.count(), 2)
        for et in Tag.objects.all():
            self.assertEqual(et.example, example)
            self.assertIn(et.key, tags)
            self.assertEqual(et.value, str(tags[et.key]))

    def test_tags_long(self) -> None:
        Example.objects.all().delete()
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        tags = {"a" * 10000: "b" * 10000}
        data = {
            "attachments": [{"url": "xxx"}],
            "tags": tags,
        }
        response = APIClient().post(path, data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Tag.objects.count(), 1)
        et: Tag = Tag.objects.first()  # type: ignore
        self.assertEqual(et.key, "a" * Tag.key_max_length)
        self.assertEqual(et.value, "b" * Tag.value_max_length)

    def test_timestamp(self) -> None:
        Example.objects.all().delete()
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        data = {
            "attachments": [{"url": "xxx"}],
            "timestamp": "2011-05-02T17:41:36Z",
        }
        response = APIClient().post(path, data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Example.objects.count(), 1)
        example: Example = Example.objects.first()  # type: ignore
        self.assertEqual(example.created_at, parser.parse(data["timestamp"]))

    def test_attachments_invalid(self) -> None:
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        invalid_data = [
            {"attachments": ""},
            {"attachments": []},
            {"attachments": [""]},
            {"attachments": {}},
            {"attachments": [{"type": "xxx"}]},
            {"attachments": [{"type": "image"}]},
            {"attachments": [{"url": "xxx", "type": "yyy"}]},
        ]
        for data in invalid_data:
            Example.objects.all().delete()
            response = APIClient().post(path, data, format="json")
            self.assertEqual(response.status_code, 400)

    def test_attachments_ok(self) -> None:
        Example.objects.all().delete()
        project = ProjectFactory.create()
        path = f"/api/capture/{project.id}/"
        data = {
            "attachments": [
                {"url": "url1"},  # default type
                {"url": "url2", "type": "image"},
                {"url": "url3", "type": "video"},
                {"url": "url4", "type": "audio"},
                {"url": "url5", "type": "text"},
            ]
        }
        response = APIClient().post(path, data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, 200)
        example: Example = Example.objects.first()  # type: ignore
        self.assertEqual(Attachment.objects.count(), 5)
        self.assertEqual(example.attachment_set.count(), 5)  # type: ignore

    def test_archived_project(self) -> None:
        project = ProjectFactory.create()
        project.archive()
        path = f"/api/capture/{project.id}/"
        data = {
            "attachments": [{"url": "http://example.com"}],
        }
        response = APIClient().post(path, data, format="json")
        print(response.json())
        self.assertEqual(response.status_code, 403)
