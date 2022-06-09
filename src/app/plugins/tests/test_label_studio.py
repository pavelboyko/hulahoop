from django.test import TestCase
from app.models.idof import IdOfProject
from app.plugins.base import ConfigError
from app.utils.rest_client import RestClient
from app.plugins.label_studio import LabelStudioPlugin


class LabelStudioPluginTest(TestCase):
    """
    ./manage.py test app.plugins.tests.test_label_studio.LabelStudioPluginTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test_config_type(self) -> None:
        self.assertRaises(
            ConfigError, LabelStudioPlugin, project_id=IdOfProject(), config=None
        )
        self.assertRaises(
            ConfigError, LabelStudioPlugin, project_id=IdOfProject(), config=""
        )
        self.assertRaises(
            ConfigError, LabelStudioPlugin, project_id=IdOfProject(), config=[]
        )
        self.assertRaises(
            ConfigError, LabelStudioPlugin, project_id=IdOfProject(), config={}
        )

    def test_config_url(self) -> None:
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_url,
            config={},
        )
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_url,
            config={"url": ""},
        )
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_url,
            config={"url": "xxx.yz"},
        )
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_url,
            config={"url": "example.com"},
        )
        try:
            LabelStudioPlugin.read_config_url({"url": "https://example.com"})
        except ConfigError as e:
            self.fail(f"Unexpected ConfigError exception: {e}")

    def test_config_api_key(self) -> None:
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_api_key,
            config={},
        )
        try:
            LabelStudioPlugin.read_config_api_key({"api_key": "xxx"})
        except ConfigError as e:
            self.fail(f"Unexpected ConfigError exception: {e}")

    def test_config_project_id(self) -> None:
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_project_id,
            config={},
        )
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_project_id,
            config={"project_id": "100"},
        )
        self.assertRaises(
            ConfigError,
            LabelStudioPlugin.read_config_project_id,
            config={"project_id": -1},
        )
        try:
            LabelStudioPlugin.read_config_project_id({"project_id": 0})
        except ConfigError as e:
            self.fail(f"Unexpected ConfigError exception: {e}")

    def test_config_ok(self) -> None:
        self.assertRaises(
            RestClient.RequestError,
            LabelStudioPlugin,
            project_id=IdOfProject(),
            config={"url": "http://localhost:8080", "api_key": "xxx", "project_id": 1},
        )
