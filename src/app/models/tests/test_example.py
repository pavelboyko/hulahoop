from django.test import TestCase
from django.utils import timezone
from app.models import Project, Example, Issue
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
        example = ExampleFactory(project=project, issue=issue)
        self.assertEqual(str(example), str(example.id)[:8])

    def test_set_labeling_completed(self) -> None:
        project = ProjectFactory.create()
        example = ExampleFactory.create(project=project)
        example.set_labeling_completed(result="test")
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.completed)

    def test_set_labeling_error(self) -> None:
        project: Project = ProjectFactory.create()
        example: Example = ExampleFactory.create(project=project)
        example.set_labeling_error(message="test")
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.error)

    def test_set_labeling_started(self) -> None:
        project: Project = ProjectFactory.create()
        example: Example = ExampleFactory.create(project=project)
        example.set_labeling_started()
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.started)

    def test_set_labeling_updated(self) -> None:
        project: Project = ProjectFactory.create()
        example: Example = ExampleFactory.create(project=project)
        example.set_labeling_updated(result="test")
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.pending)

    def test_set_labeling_deleted(self) -> None:
        project: Project = ProjectFactory.create()
        example: Example = ExampleFactory.create(project=project)
        example.set_labeling_deleted()
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.started)
