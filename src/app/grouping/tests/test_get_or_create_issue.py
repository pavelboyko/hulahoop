from django.test import TestCase
from app.models import Project, Issue, Example, example
from app.fixtures import ProjectFactory, IssueFactory, ExampleFactory
from app.grouping import get_or_create_issue


class Test(TestCase):
    """
    ./manage.py test app.grouping.tests.test_get_or_create_issue.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_no_fingerprint(self) -> None:
        project = ProjectFactory.create()
        example = ExampleFactory.create(project=project)
        issue, is_created = get_or_create_issue(example)
        self.assertIsNone(issue)
        self.assertFalse(is_created)

    def test_create(self) -> None:
        project = ProjectFactory.create()
        example = ExampleFactory.create(project=project, fingerprint="xxx")
        issue, is_created = get_or_create_issue(example)
        self.assertIsNotNone(issue)
        self.assertEqual(issue.fingerprint, example.fingerprint)
        self.assertTrue(is_created)

    def test_get(self) -> None:
        project = ProjectFactory.create()
        example1 = ExampleFactory.create(project=project, fingerprint="xxx")
        example2 = ExampleFactory.create(project=project, fingerprint="xxx")
        issue1, _ = get_or_create_issue(example1)
        issue2, is_created = get_or_create_issue(example2)
        self.assertEqual(issue1, issue2)
        self.assertFalse(is_created)
