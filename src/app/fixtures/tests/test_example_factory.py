from django.test import TestCase
from app.models import Project
from app.fixtures import ExampleFactory, IssueFactory


class Test(TestCase):
    """
    ./manage.py test app.fixtures.tests.test_example_factory.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_without_issue(self) -> None:
        example = ExampleFactory()
        self.assertIsNotNone(example.project)
        self.assertIsNone(example.issue)

    def test_with_issue(self) -> None:
        issue = IssueFactory()
        example = ExampleFactory(project=issue.project, issue=issue)
        self.assertIsNotNone(example.project)
        self.assertIsNotNone(example.issue)
        self.assertEqual(example.project, issue.project)
