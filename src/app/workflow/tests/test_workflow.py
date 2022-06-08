from django.test import TestCase
from app.models.idof import IdOfProject
from app.models import Project, Issue, Example
from app.fixtures import ProjectFactory, IssueFactory, ExampleFactory
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

    def test_start(self) -> None:
        project = ProjectFactory(properties={})
        labeling_plugin = DummyLabelingPlugin(project_id=project.id)
        wf = Workflow(project_id=project.id, labeling_plugin=labeling_plugin)
        example = ExampleFactory(project=project)
        wf.start(example.id)
        # our dummy labeling plugin immediately marks examples as completed on start
        example.refresh_from_db()
        self.assertEqual(example.status, Example.Status.completed.value)
