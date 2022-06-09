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

valid_config = {"url": "http://example.com", "api_key": "xxx", "project_id": 1}


def create_plugin(project_id: IdOfProject = IdOfProject()):
    return LabelStudioPlugin(project_id=project_id, config=valid_config)


class LabelStudioPluginTest(TestCase):
    """
    ./manage.py test app.plugins.tests.test_label_studio.LabelStudioPluginTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test_validate_config(self) -> None:
        invalid_configs = [
            None,
            [],
            "",
            {},
            {"url": "", "api_key": "", "project_id": -1},
            {"url": "", "api_key": "", "project_id": 0},
            {"url": "xxx", "api_key": "", "project_id": 0},
            {"url": "www.example.com", "api_key": "", "project_id": 0},
        ]
        for config in invalid_configs:
            print(config)
            self.assertRaises(ConfigError, LabelStudioPlugin.validate_config, config)

        self.assertEqual(LabelStudioPlugin.validate_config(valid_config), valid_config)

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
                        "project": valid_config["project_id"],
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
        except RestClient.RequestError as e:  # pragma: no cover
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
        except RestClient.RequestError as e:  # pragma: no cover
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
