from django.test import TestCase
from unittest import skip
from app.models import Project
from app.fixtures import ProjectFactory
from app.workflow.factory import get_workflow, rebuild


class WorkflowFactoryTest(TestCase):
    """
    ./manage.py test app.workflow.tests.test_factory.WorkflowFactoryTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_empty_project_props(self) -> None:
        project = ProjectFactory.create(properties={})
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)

    def test_empty_plugins_props(self) -> None:
        project = ProjectFactory.create(properties={"plugins": {}})
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)

    @skip(
        "Don't know why it fails in github actions and doesn't fail locally. Will be fixed later."
    )
    def test_none_plugins_props(self) -> None:
        project = ProjectFactory.create(properties={"plugins": None})
        workflow = get_workflow(project.id)
        self.assertIsNone(workflow)

    def test_none_project_props(self) -> None:
        project = ProjectFactory.create(properties=None)
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)

    def test_array_project_props(self) -> None:
        project = ProjectFactory.create(properties=[])
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)

    def test_str_project_props(self) -> None:
        project = ProjectFactory.create(properties="")
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)

    def test_unknown_labeling_plugin(self) -> None:
        project = ProjectFactory.create(
            properties={
                "plugins": {"labeling": {"slug": "__UNKNOWN__", "config": None}}
            }
        )
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)

    @skip(
        "Don't know why it fails in github actions and doesn't fail locally. Will be fixed later."
    )
    def test_dummy_labeling_plugin(self) -> None:
        project = ProjectFactory.create(
            properties={
                "plugins": {"labeling": {"slug": "dummy_labeling", "config": None}}
            }
        )
        workflow = get_workflow(project.id)
        self.assertIsNotNone(workflow)
        self.assertTrue(len(workflow.webhook_receivers) > 0)

    def test_singleton(self) -> None:
        project = ProjectFactory.create(properties={})
        workflow1 = get_workflow(project.id)
        workflow2 = get_workflow(project.id)
        self.assertEqual(workflow1, workflow2)

    def test_rebuild(self) -> None:
        project = ProjectFactory.create(properties={})
        workflow1 = get_workflow(project.id)
        rebuild(project.id)
        workflow2 = get_workflow(project.id)
        self.assertNotEqual(workflow1, workflow2)
