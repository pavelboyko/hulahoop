from cgi import test


from django.test import TestCase
from app.models import Project
from app.fixtures import ExampleFactory, ProjectFactory, IssueFactory


class Test(TestCase):
    """
    ./manage.py test app.models.tests.test_project.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_str(self) -> None:
        project = ProjectFactory.create()
        self.assertEqual(str(project), project.name)

    def test_example_count(self) -> None:
        example = ExampleFactory.create()
        self.assertEqual(example.project.example_count(), 1)

    def test_issue_count(self) -> None:
        issue = IssueFactory.create()
        self.assertEqual(issue.project.issue_count(), 1)
