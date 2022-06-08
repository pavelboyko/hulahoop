from django.test import TestCase
from app.models import Project
from app.fixtures import ProjectFactory
from app.workflow.factory import get_workflow


class WorkflowFactoryTest(TestCase):
    """
    ./manage.py test app.workflow.tests.test_factory.WorkflowFactoryTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_get_workflow(self) -> None:
        project = ProjectFactory()
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)
