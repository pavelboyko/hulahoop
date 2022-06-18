from django.test import TestCase, Client
from django.urls import reverse
from app.fixtures import IssueFactory
from app.models import Project, User


class Test(TestCase):
    """
    ./manage.py test mpa.views.issue.tests.test_detail.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_login_required(self) -> None:
        response = Client().get(reverse("issue_detail", args=[0, 0]))
        self.assertEqual(response.status_code, 302)

    def test_get(self) -> None:
        issue = IssueFactory.create(examples=10)
        client = Client()
        client.force_login(User.objects.last())  # type: ignore
        response = client.get(
            reverse("issue_detail", args=[issue.project.id, issue.id])
        )
        self.assertEqual(response.status_code, 200)
