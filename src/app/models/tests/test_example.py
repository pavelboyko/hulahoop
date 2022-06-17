from django.test import TestCase
from app.models import Project, Example
from app.fixtures import ProjectFactory, IssueFactory, ExampleFactory


class ExampleTest(TestCase):
    """
    ./manage.py test app.models.tests.test_example.ExampleTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_create(self) -> None:
        project = ProjectFactory()
        issue = IssueFactory(project=project)
        example: Example = ExampleFactory(project=project, issue=issue)  # type: ignore
        self.assertEqual(str(example), str(example.id)[:8])
