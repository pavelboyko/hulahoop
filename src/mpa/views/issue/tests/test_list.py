from django.test import TestCase, Client
from django.urls import reverse
from app.fixtures import ProjectFactory, IssueFactory
from app.models import Project, User
from app.models.issue import Issue


class Test(TestCase):
    """
    ./manage.py test mpa.views.issue.tests.test_list.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_login_required(self) -> None:
        response = Client().get(reverse("issue_list", args=[0]))
        self.assertEqual(response.status_code, 302)

    def test_get(self) -> None:
        project = ProjectFactory.create()
        for _ in range(5):
            IssueFactory.create(project=project)
        client = Client()
        client.force_login(User.objects.last())  # type: ignore
        response = client.get(reverse("issue_list", args=[project.id]))
        self.assertEqual(response.status_code, 200)
