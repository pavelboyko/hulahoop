from django.test import TestCase
from app.fixtures import IssueFactory, ProjectFactory


class Test(TestCase):
    """
    ./manage.py test app.fixtures.tests.test_issue_factory.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test(self) -> None:
        issue = IssueFactory()
        self.assertIsNotNone(issue.name)
        self.assertIsNotNone(issue.description)

    def test_with_project(self) -> None:
        project = ProjectFactory()
        issue = IssueFactory(project=project)
        self.assertEqual(issue.project, project)
