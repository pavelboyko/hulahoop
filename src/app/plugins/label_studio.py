import logging
from typing import Dict, Any
from django.urls import reverse
from hulahoop.settings import HTTP_SCHEME, HOSTNAME
from app.models import Example
from app.models.idof import IdOfProject, IdOfExample
from app.utils.rest_client import RestClient
from .base import BaseLabelingPlugin, ConfigError

logger = logging.getLogger(__package__)


class LabelStudioPlugin(BaseLabelingPlugin):
    name: str = "Label Studio"
    slug: str = "labelstudio"

    base_url: str
    api_key: str
    ls_project_id: int

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
        logger.debug(f"Initializing {self.name} plugin config={config}")
        self.read_config(config)
        self.client = RestClient(
            base_url=self.base_url, headers={"Authorization": f"Token {self.api_key}"}
        )

        webhook_path = reverse("webhook_v1_0", args=[project_id, self.slug])
        webhook_url = f"{HTTP_SCHEME}{HOSTNAME}{webhook_path}"
        # As we init plugin in every celery worker on every start
        # make sure that our webhook wasn't already registered
        if not self.check_webhook_exists(webhook_url):
            self.create_webhook(webhook_url)

    def read_config(self, config: Dict[str, Any]) -> None:
        self.base_url = config.get("LABELSTUDIO_URL")
        if not self.base_url:
            raise ConfigError("Missing required LABELSTUDIO_URL field")

        self.api_key = config.get("LABELSTUDIO_API_KEY")
        if not self.api_key:
            raise ConfigError("Missing required LABELSTUDIO_API_KEY field")

        self.ls_project_id = config.get("LABELSTUDIO_PROJECT_ID")
        if not self.ls_project_id:
            raise ConfigError("Missing required LABELSTUDIO_PROJECT_ID field")

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
                "actions": [
                    "ANNOTATION_CREATED",
                    "ANNOTATIONS_CREATED",
                    "ANNOTATION_UPDATED",
                    "ANNOTATIONS_DELETED",
                ],
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
