from uuid import uuid4
from django.test import TestCase, Client
from django.urls import reverse
from app.fixtures import ExampleFactory, IssueFactory
from app.models import Project, User


class Test(TestCase):
    """
    ./manage.py test mpa.views.example.tests.test_detail.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_login_required(self) -> None:
        response = Client().get(reverse("example_detail", args=[0, uuid4()]))
        self.assertEqual(response.status_code, 302)

    def test_with_issue(self) -> None:
        issue = IssueFactory.create()
        example = ExampleFactory.create(project=issue.project, issue=issue)
        client = Client()
        client.force_login(User.objects.last())  # type: ignore
        response = client.get(
            reverse("example_detail", args=[example.project.id, example.id])
        )
        self.assertEqual(response.status_code, 200)

    def test_without_issue(self) -> None:
        example = ExampleFactory.create()
        client = Client()
        client.force_login(User.objects.last())  # type: ignore
        response = client.get(
            reverse("example_detail", args=[example.project.id, example.id])
        )
        self.assertEqual(response.status_code, 200)
