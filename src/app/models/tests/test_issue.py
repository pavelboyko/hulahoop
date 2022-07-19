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
            project=issue.project, timestamp=timezone.now() - timedelta(days=1)
        )
        example2: Example = ExampleFactory.create(
            project=issue.project, timestamp=timezone.now() + timedelta(days=1)
        )
        self.assertEqual(issue.example_set.count(), 0)  # type: ignore
        issue.add_example(example1)
        issue.refresh_from_db()
        self.assertEqual(issue.first_seen, example1.timestamp)
        self.assertEqual(issue.last_seen, example1.timestamp)

        issue.add_example(example2)
        issue.refresh_from_db()
        self.assertEqual(issue.example_set.count(), 2)  # type: ignore
        self.assertEqual(issue.first_seen, example1.timestamp)
        self.assertEqual(issue.last_seen, example2.timestamp)

    def test_reopen_at_add_example(self) -> None:
        issue: Issue = IssueFactory.create()
        issue.resolve()
        example: Example = ExampleFactory.create(project=issue.project)
        issue.add_example(example)
        issue.refresh_from_db()
        self.assertEqual(issue.status, Issue.Status.open)

    def test_do_not_reopen_closed(self) -> None:
        issue: Issue = IssueFactory.create()
        issue.close()
        example: Example = ExampleFactory.create(project=issue.project)
        issue.add_example(example)
        issue.refresh_from_db()
        self.assertEqual(issue.status, Issue.Status.closed)

    def test_mute(self) -> None:
        issue: Issue = IssueFactory.create()
        issue.mute()
        issue.refresh_from_db()
        self.assertEqual(issue.status, Issue.Status.muted)

    def test_close(self) -> None:
        issue: Issue = IssueFactory.create()
        issue.close()
        issue.refresh_from_db()
        self.assertEqual(issue.status, Issue.Status.closed)

    def test_reopen(self) -> None:
        issue: Issue = IssueFactory.create()
        issue.reopen()
        issue.refresh_from_db()
        self.assertEqual(issue.status, Issue.Status.open)

    def test_resolve(self) -> None:
        issue: Issue = IssueFactory.create()
        issue.resolve()
        issue.refresh_from_db()
        self.assertEqual(issue.status, Issue.Status.resolved)
