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
        project = ProjectFactory.create(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        self.assertIsNotNone(wf)

    def test_start_unknown_example(self) -> None:
        project = ProjectFactory.create(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        wf.start(uuid4())

    def test_start_without_labeling_plugin(self) -> None:
        project = ProjectFactory.create(properties={})
        wf = Workflow(project_id=project.id, labeling_plugin=None)
        example = ExampleFactory.create(project=project)
        wf.start(example.id)

    def test_start(self) -> None:
        project = ProjectFactory.create(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        example = ExampleFactory.create(project=project)
        wf.start(example.id)

    def test_on_annotation_updated(self) -> None:
        wf = Workflow(project_id=IdOfProject(), labeling_plugin=None)
        project = ProjectFactory.create(properties={})
        example: Example = ExampleFactory.create(project=project)
        wf.on_labeling_event(
            example=example,
            event=BaseLabelingPlugin.Event.annotation_updated,
            result="test",
        )

    def test_on_annotation_deleted(self) -> None:
        wf = Workflow(project_id=IdOfProject(), labeling_plugin=None)
        project = ProjectFactory.create(properties={})
        example = ExampleFactory.create(project=project)
        wf.on_labeling_event(
            example=example,
            event=BaseLabelingPlugin.Event.annotation_deleted,
            result="test",
        )

    def test_labeling_exception(self) -> None:
        project = ProjectFactory.create(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        wf.label_example(example=None)  # type: ignore

    def test_grouping(self) -> None:
        project = ProjectFactory.create(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        example = ExampleFactory.create(project=project, fingerprint="xxx")
        wf.start(example.id)
        example.refresh_from_db()
        self.assertIsNotNone(example.issue)
        self.assertEquals(example.fingerprint, example.issue.fingerprint)
