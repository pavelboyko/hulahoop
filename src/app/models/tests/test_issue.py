from django.test import TestCase
from app.models import Issue
from app.fixtures import IssueFactory, ExampleFactory


class Test(TestCase):
    """
    ./manage.py test app.models.tests.test_issue.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Issue.objects.all().delete()

    def test_str(self) -> None:
        issue = IssueFactory.create()
        self.assertEqual(str(issue), f"#{issue.id}")

    def test_example_count(self) -> None:
        issue = IssueFactory.create()
        example = ExampleFactory.create(project=issue.project, issue=issue)
        self.assertEqual(issue.example_count(), 1)
