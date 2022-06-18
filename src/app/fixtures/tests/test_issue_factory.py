from django.test import TestCase
from app.models import Project, Example
from app.fixtures import IssueFactory, ProjectFactory


class Test(TestCase):
    """
    ./manage.py test app.fixtures.tests.test_issue_factory.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test(self) -> None:
        issue = IssueFactory()
        self.assertIsNotNone(issue.name)

    def test_with_project(self) -> None:
        project = ProjectFactory()
        issue = IssueFactory(project=project)
        self.assertEqual(issue.project, project)

    def test_with_examples(self) -> None:
        issue = IssueFactory(examples=10)
        self.assertEqual(Example.objects.count(), 10)
        for e in Example.objects.all():
            self.assertEqual(e.issue, issue)
            self.assertEqual(e.project, issue.project)
