from typing import Any
import uuid
import requests
import responses
from responses import matchers
from django.test import TestCase
from hulahoop.settings import HTTP_SCHEME, HOSTNAME
from app.models.idof import IdOfProject
from app.plugins.base import BaseLabelingPlugin, ConfigError
from app.utils.rest_client import RestClient
from app.fixtures import ProjectFactory, ExampleFactory
from app.models import Project, Example
from app.plugins.label_studio import LabelStudioPlugin

valid_config = {"url": "http://example.com", "api_key": "xxx", "project_id": 1}


def create_plugin(project_id: IdOfProject = IdOfProject()) -> LabelStudioPlugin:
    return LabelStudioPlugin(project_id=project_id, config=valid_config)


@responses.activate
def create_plugin_with_webook(
    project_id: IdOfProject = IdOfProject(),
) -> LabelStudioPlugin:
    responses.get(url="http://example.com/api/webhooks/", json={}, status=200)
    responses.post(url="http://example.com/api/webhooks/", json={}, status=201)
    return create_plugin(project_id)


class LabelStudioPluginTest(TestCase):
    """
    ./manage.py test app.plugins.tests.test_label_studio.LabelStudioPluginTest --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

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
                        "url": f"{HTTP_SCHEME}{HOSTNAME}/api/webhook/{IdOfProject()}/label_studio/",
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
            json=[{"url": f"{HTTP_SCHEME}{HOSTNAME}/api/webhook/0/label_studio/"}],
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
        project = ProjectFactory.create(
            properties={"plugins": {"labeling": valid_config}}
        )
        example = ExampleFactory.create(project=project)

        responses.get(url="http://example.com/api/webhooks/", json={}, status=200)
        responses.post(url="http://example.com/api/webhooks/", json={}, status=201)
        req = responses.post(
            url=f"http://example.com/api/projects/{valid_config['project_id']}/import",
            json={},
            status=201,
            match=[
                matchers.json_params_matcher(
                    {
                        "image": example.get_display_image(),
                        LabelStudioPlugin.token_field: str(example.id),
                    }
                )
            ],
        )

        plugin = create_plugin(project.id)
        plugin.create_task(example)
        self.assertEqual(req.call_count, 1)

    def test_receive_webhook_nocallback(self) -> None:
        example = ExampleFactory.create()
        plugin = create_plugin_with_webook()
        plugin.receive_webhook(
            data={
                "task": {
                    "data": {LabelStudioPlugin.token_field: str(example.id)},
                },
                "action": "ANNOTATION_CREATED",
                "annotation": {},
            }
        )

    def callback(
        self, example: Example, action: BaseLabelingPlugin.Event, result: Any
    ) -> None:
        self.assertEqual(action, BaseLabelingPlugin.Event.annotation_created)
        self.assertEqual(result, "RESULT")

    def test_receive_webhook(self) -> None:
        example = ExampleFactory.create()
        plugin = create_plugin_with_webook()
        plugin.callback = self.callback
        plugin.receive_webhook(
            data={
                "task": {
                    "data": {LabelStudioPlugin.token_field: str(example.id)},
                },
                "action": "ANNOTATION_CREATED",
                "annotation": "RESULT",
            }
        )

    def test_receive_webhook_noexample(self) -> None:
        plugin = create_plugin_with_webook()
        # should not crash
        plugin.receive_webhook(
            data={
                "task": {
                    "data": {LabelStudioPlugin.token_field: str(uuid.uuid4())},
                },
                "action": "ANNOTATION_CREATED",
                "annotation": "RESULT",
            }
        )

    def test_receive_webhook_invalid(self) -> None:
        plugin = create_plugin_with_webook()
        # should not crash
        plugin.receive_webhook(data={})
