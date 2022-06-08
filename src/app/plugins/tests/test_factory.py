from django.test import TestCase
from app.plugins.factory import build_labeling_plugin


class WorkflowFactoryTest(TestCase):
    """
    ./manage.py test app.plugins.tests.test_factory.WorkflowFactoryTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test_unknown(self) -> None:
        plugin = build_labeling_plugin(slug="___UNKNOWN___", project_id=0, config={})
        self.assertIsNone(plugin)

    def test_build_dummy_labeling_plugin(self) -> None:
        plugin = build_labeling_plugin(slug="dummy_labeling", project_id=0, config={})
        self.assertIsNotNone(plugin)
        self.assertEqual(plugin.slug, "dummy_labeling")
