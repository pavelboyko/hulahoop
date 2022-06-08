from django.test import TestCase
from django.utils import timezone
from app.models import Project, Example, Issue, ExampleEvent
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
        project: Project = ProjectFactory()
        example: Example = ExampleFactory(project=project)
        example.set_labeling_completed(result="test")
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.completed)
        self.assertEqual(ExampleEvent.objects.all().count(), 1)
        ee: ExampleEvent = ExampleEvent.objects.first()
        self.assertEqual(ee.example, example)
        self.assertEqual(ee.event_type, ExampleEvent.EventType.labeling_completed)
        self.assertDictEqual(ee.properties, {"result": "test"})

    def test_set_labeling_error(self) -> None:
        project: Project = ProjectFactory()
        example: Example = ExampleFactory(project=project)
        example.set_labeling_error(message="test")
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.error)
        self.assertEqual(ExampleEvent.objects.all().count(), 1)
        ee: ExampleEvent = ExampleEvent.objects.first()
        self.assertEqual(ee.example, example)
        self.assertEqual(ee.event_type, ExampleEvent.EventType.labeling_error)
        self.assertDictEqual(ee.properties, {"message": "test"})

    def test_set_labeling_started(self) -> None:
        project: Project = ProjectFactory()
        example: Example = ExampleFactory(project=project)
        example.set_labeling_started()
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.started)
        self.assertEqual(ExampleEvent.objects.all().count(), 1)
        ee: ExampleEvent = ExampleEvent.objects.first()
        self.assertEqual(ee.example, example)
        self.assertEqual(ee.event_type, ExampleEvent.EventType.labeling_started)

    def test_set_labeling_updated(self) -> None:
        project: Project = ProjectFactory()
        example: Example = ExampleFactory(project=project)
        example.set_labeling_updated(result="test")
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.pending)
        self.assertEqual(ExampleEvent.objects.all().count(), 1)
        ee: ExampleEvent = ExampleEvent.objects.first()
        self.assertEqual(ee.example, example)
        self.assertEqual(ee.event_type, ExampleEvent.EventType.labeling_updated)
        self.assertDictEqual(ee.properties, {"result": "test"})

    def test_set_labeling_deleted(self) -> None:
        project: Project = ProjectFactory()
        example: Example = ExampleFactory(project=project)
        example.set_labeling_deleted()
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.started)
        self.assertEqual(ExampleEvent.objects.all().count(), 1)
        ee: ExampleEvent = ExampleEvent.objects.first()
        self.assertEqual(ee.example, example)
        self.assertEqual(ee.event_type, ExampleEvent.EventType.labeling_deleted)
