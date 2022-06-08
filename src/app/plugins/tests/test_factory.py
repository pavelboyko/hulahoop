from django.test import TestCase
from app.plugins.factory import build_labeling_plugin


class WorkflowFactoryTest(TestCase):
    """
    ./manage.py test app.plugins.tests.test_factory.WorkflowFactoryTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test_unknown(self) -> None:
        plugin = build_labeling_plugin(project_id=0, slug="___UNKNOWN___", config={})
        self.assertIsNone(plugin)

    def test_build_dummy_labeling_plugin(self) -> None:
        plugin = build_labeling_plugin(project_id=0, slug="dummy_labeling", config={})
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.slug, "dummy_labeling")
