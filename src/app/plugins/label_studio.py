import logging
from typing import Dict, Any
from django.urls import reverse
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from hulahoop.settings import HTTP_SCHEME, HOSTNAME
from app.models import Example
from app.models.idof import IdOfProject, IdOfExample
from app.utils.rest_client import RestClient
from .base import BaseLabelingPlugin, ConfigError

logger = logging.getLogger(__package__)


class LabelStudioPlugin(BaseLabelingPlugin):
    name: str = "Label Studio"
    slug: str = "label_studio"

    base_url: str = ""
    api_key: str = ""
    ls_project_id: int = -1

    token_field: str = "hulahoop_example_id"
    event_map: Dict[str, BaseLabelingPlugin.Event] = {
        "ANNOTATION_CREATED": BaseLabelingPlugin.Event.annotation_created,
        "ANNOTATIONS_CREATED": BaseLabelingPlugin.Event.annotation_created,
        "ANNOTATION_UPDATED": BaseLabelingPlugin.Event.annotation_updated,
        "ANNOTATIONS_UPDATED": BaseLabelingPlugin.Event.annotation_updated,
        "ANNOTATIONS_DELETED": BaseLabelingPlugin.Event.annotation_deleted,
    }

    client: RestClient

    def __init__(self, project_id: IdOfProject, config: Any):
        super().__init__(project_id, config)
        logger.debug(f"Initializing {self.name} plugin config={config}")
        if not isinstance(config, dict):
            raise ConfigError("Plugin config must be a dict")

        self.base_url = LabelStudioPlugin.read_config_url(config)
        self.api_key = LabelStudioPlugin.read_config_api_key(config)
        self.ls_project_id = LabelStudioPlugin.read_config_project_id(config)

        self.client = RestClient(
            base_url=self.base_url, headers={"Authorization": f"Token {self.api_key}"}
        )

        webhook_path = reverse("webhook_v1_0", args=[project_id, self.slug])
        webhook_url = f"{HTTP_SCHEME}{HOSTNAME}{webhook_path}"
        # As we init plugin in every celery worker on every start
        # make sure that our webhook wasn't already registered
        if not self.check_webhook_exists(webhook_url):
            self.create_webhook(webhook_url)

    def create_task(self, example: Example) -> None:
        logger.debug(f"Creating {self.name} task for example_id={example.id}")
        # Assume all examples are images for a while
        self.client.create(
            path=f"/api/projects/{self.ls_project_id}/import",  # NB! no slash at the end
            data={"image": example.media_url, self.token_field: str(example.id)},
        )

    def check_webhook_exists(self, url: str) -> bool:
        """Check if a given webhook url already registered in Label Studio"""
        try:
            webhooks = self.client.get(path="/api/webhooks/")
            for wh in webhooks:
                if wh["url"] == url:
                    return True
            return False
        except (TypeError, ValueError, KeyError) as e:
            raise RestClient.RequestError(e)

    def create_webhook(self, url: str) -> None:
        """Register webhook in Label Studio"""
        logger.debug(f"Registering {self.name} webhook url={url}")
        self.client.create(
            path="/api/webhooks/",
            data={
                "project": self.ls_project_id,
                "url": url,
                "send_payload": True,
                "send_for_all_actions": False,
                "actions": (
                    "ANNOTATION_CREATED",
                    "ANNOTATIONS_CREATED",
                    "ANNOTATION_UPDATED",
                    "ANNOTATIONS_UPDATED",
                    "ANNOTATIONS_DELETED",
                ),
            },
        )

    def receive_webhook(self, data: Any) -> None:
        try:
            example_id = IdOfExample(data["task"]["data"][self.token_field])
            example = Example.objects.get(id=example_id)
            action = self.event_map[data["action"]]
            result = data["annotation"]
            if self.callback:
                self.callback(example, action, result)
            else:
                logger.warning(
                    f"{self.name} plugin received a webhook but callback is not set. This looks like a programming error."
                )
        except (ValueError, KeyError, TypeError):
            logger.error(
                f"{self.name} plugin can't parse webhook request: {data}. Skipped."
            )

        # FIXME: catch exceptions from Example.objects.get

    @staticmethod
    def read_config_url(config: Dict[str, Any]) -> str:
        url = config.get("url")
        if url is None:
            raise ConfigError("Missing required 'url' field")

        validate_url = URLValidator()
        try:
            validate_url(url)
        except ValidationError as e:
            raise ConfigError("'url' field value is not a valid URL: {e}")

        return url

    @staticmethod
    def read_config_api_key(config: Dict[str, Any]) -> str:
        api_key = config.get("api_key")
        if api_key is None:
            raise ConfigError("Missing required 'api_key' field")
        return api_key

    @staticmethod
    def read_config_project_id(config: Dict[str, Any]) -> int:
        project_id = config.get("project_id")
        if project_id is None:
            raise ConfigError("Missing required 'project_id' field")
        if not isinstance(project_id, int):
            raise ConfigError("'project_id' field must be int: {project_id}")
        if project_id < 0:
            raise ConfigError("'project_id' field must be positive: {project_id}")
        return project_id
