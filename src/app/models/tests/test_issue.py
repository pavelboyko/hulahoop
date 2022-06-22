from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from app.models import Issue, Example
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

    def test_add_example(self) -> None:
        issue: Issue = IssueFactory.create()
        example1: Example = ExampleFactory.create(
            project=issue.project, created_at=timezone.now() - timedelta(days=1)
        )
        example2: Example = ExampleFactory.create(
            project=issue.project, created_at=timezone.now() + timedelta(days=1)
        )
        self.assertEqual(issue.example_set.count(), 0)  # type: ignore
        issue.add_example(example1)
        issue.add_example(example2)
        issue.refresh_from_db()
        self.assertEqual(issue.example_set.count(), 2)  # type: ignore
        self.assertEqual(issue.first_seen, example1.created_at)
        self.assertEqual(issue.last_seen, example2.created_at)
