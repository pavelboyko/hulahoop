from django.test import TestCase
from uuid import uuid4
from app.models.idof import IdOfProject
from app.models import Project, Example
from app.fixtures import ProjectFactory, ExampleFactory
from app.plugins import BaseLabelingPlugin
from app.plugins.dummy import DummyLabelingPlugin
from app.workflow.workflow import Workflow


class WorkflowTest(TestCase):
    """
    ./manage.py test app.workflow.tests.test_workflow.WorkflowTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_init_none(self) -> None:
        wf = Workflow(project_id=IdOfProject(), labeling_plugin=None)
        self.assertIsNotNone(wf)

    def test_init(self) -> None:
        project = ProjectFactory(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        self.assertIsNotNone(wf)

    def test_start_unknown_example(self) -> None:
        project = ProjectFactory(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        wf.start(uuid4())

    def test_start_without_labeling_plugin(self) -> None:
        project = ProjectFactory(properties={})
        wf = Workflow(project_id=project.id, labeling_plugin=None)
        example = ExampleFactory(project=project)
        wf.start(example.id)
        # without a labeling plugin example should remain "pending"
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.pending.value)

    def test_start(self) -> None:
        project = ProjectFactory(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        example = ExampleFactory(project=project)
        wf.start(example.id)
        # our dummy labeling plugin immediately marks examples as completed on start
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.completed.value)

    def test_on_annotation_updated(self) -> None:
        wf = Workflow(project_id=IdOfProject(), labeling_plugin=None)
        project = ProjectFactory(properties={})
        example: Example = ExampleFactory(project=project)
        wf.on_labeling_event(
            example=example,
            event=BaseLabelingPlugin.Event.annotation_updated,
            result="test",
        )
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.pending)

    def test_on_annotation_deleted(self) -> None:
        wf = Workflow(project_id=IdOfProject(), labeling_plugin=None)
        project = ProjectFactory(properties={})
        example: Example = ExampleFactory(project=project)
        wf.on_labeling_event(
            example=example,
            event=BaseLabelingPlugin.Event.annotation_deleted,
            result="test",
        )
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.started)

    def test_labeling_exception(self) -> None:
        project = ProjectFactory(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        wf.label_example(example=None)  # don't crash
