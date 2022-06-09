from django.test import TestCase
import requests
import responses
from responses import matchers
from hulahoop.settings import HTTP_SCHEME, HOSTNAME
from app.models.idof import IdOfProject
from app.plugins.base import ConfigError
from app.utils.rest_client import RestClient
from app.fixtures import ProjectFactory, ExampleFactory
from app.models import Project, Example
from app.plugins.label_studio import LabelStudioPlugin

correct_config = {"url": "http://example.com", "api_key": "xxx", "project_id": 1}


def create_plugin(project_id: IdOfProject = IdOfProject()):
    return LabelStudioPlugin(project_id=project_id, config=correct_config)


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
            LabelStudioPlugin.read_config_url({"url": "https://example.com:8080"})
            LabelStudioPlugin.read_config_url({"url": "http://localhost:8080"})
            LabelStudioPlugin.read_config_url(
                {"url": "http://host.docker.internal:8080/"}
            )
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

    @responses.activate
    def test_webhook_create(self) -> None:
        responses.get(url="http://example.com/api/webhooks/", json={}, status=200)
        responses.post(
            url="http://example.com/api/webhooks/",
            json={},
            status=201,
            match=[
                matchers.json_params_matcher(
                    {
                        "project": correct_config["project_id"],
                        "url": f"{HTTP_SCHEME}{HOSTNAME}/api/v1.0/webhook/{IdOfProject()}/label_studio/",
                        "send_for_all_actions": False,
                        "send_payload": True,
                        "actions": [
                            "ANNOTATION_CREATED",
                            "ANNOTATIONS_CREATED",
                            "ANNOTATION_UPDATED",
                            "ANNOTATIONS_UPDATED",
                            "ANNOTATIONS_DELETED",
                        ],
                    }
                )
            ],
        )
        try:
            create_plugin()
        except RestClient.RequestError as e:
            self.fail(f"Unexpected request error: {e}")

    @responses.activate
    def test_webhook_exists(self) -> None:
        responses.get(
            url="http://example.com/api/webhooks/",
            json=[{"url": f"{HTTP_SCHEME}{HOSTNAME}/api/v1.0/webhook/0/label_studio/"}],
            status=200,
        )
        try:
            create_plugin()
        except RestClient.RequestError as e:
            self.fail(f"Unexpected request error: {e}")

    @responses.activate
    def test_webhook_status(self) -> None:
        responses.get(
            url="http://example.com/api/webhooks/",
            body={"Ooops, not found"},
            status=404,
        )
        self.assertRaises(RestClient.RequestError, create_plugin)

    @responses.activate
    def test_webhook_error(self) -> None:
        responses.get(
            url="http://example.com/api/webhooks/",
            body=requests.ConnectionError(),
        )
        self.assertRaises(RestClient.RequestError, create_plugin)

    @responses.activate
    def test_webhook_invalid_response(self) -> None:
        responses.get(
            url="http://example.com/api/webhooks/",
            json="Ooops",
            status=200,
        )
        self.assertRaises(RestClient.RequestError, create_plugin)

    @responses.activate
    def test_create_task(self) -> None:
        pass
