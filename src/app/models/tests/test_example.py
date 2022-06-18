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
        example: Example = ExampleFactory.create(project=project, issue=issue)
        self.assertEqual(str(example), str(example.id)[:8])

    def test_display_image(self) -> None:
        example: Example = ExampleFactory.create()
        self.assertIsNotNone(example.get_display_image())

    def test_no_display_image(self) -> None:
        example: Example = ExampleFactory.create(attachments=0)
        self.assertIsNone(example.get_display_image())
