import logging
from this import d
from typing import Dict, Any, Optional
from django.urls import reverse
from django.core.exceptions import MultipleObjectsReturned
from jsonschema import validate, draft7_format_checker
from jsonschema.exceptions import ValidationError
from hulahoop.settings import HTTP_SCHEME, HOSTNAME
from app.models import Example
from app.models.idof import IdOfProject, IdOfExample
from app.utils.rest_client import RestClient
from .base import BaseLabelingPlugin, ConfigError

logger = logging.getLogger(__package__)


class LabelStudioPlugin(BaseLabelingPlugin):
    name: str = "Label Studio"
    slug: str = "label_studio"

    config_schema = {
        "type": "object",
        "properties": {
            "url": {"type": "string", "format": "uri"},
            "api_key": {"type": "string"},
            "project_id": {"type": "integer", "minimum": 0},
        },
        "required": ["url", "api_key", "project_id"],
    }
    token_field: str = "hulahoop_example_id"
    event_map: Dict[str, BaseLabelingPlugin.Event] = {
        "ANNOTATION_CREATED": BaseLabelingPlugin.Event.annotation_created,
        "ANNOTATIONS_CREATED": BaseLabelingPlugin.Event.annotation_created,
        "ANNOTATION_UPDATED": BaseLabelingPlugin.Event.annotation_updated,
        # "ANNOTATIONS_UPDATED": BaseLabelingPlugin.Event.annotation_updated,
        "ANNOTATIONS_DELETED": BaseLabelingPlugin.Event.annotation_deleted,
    }

    def __init__(self, project_id: IdOfProject, config: Any):
        super().__init__(project_id, config)
        logger.debug(f"Initializing {self.name} plugin config={config}")

        self.config: Dict[str, Any] = self.validate_config(config)

        self.client = RestClient(
            base_url=self.config["url"],
            headers={"Authorization": f"Token {self.config['api_key']}"},
        )

        webhook_path = reverse("api_webhook", args=[project_id, self.slug])
        webhook_url = f"{HTTP_SCHEME}{HOSTNAME}{webhook_path}"
        # As we init plugin in every celery worker on every start
        # make sure that our webhook wasn't already registered
        if not self.check_webhook_exists(webhook_url):
            self.create_webhook(webhook_url)

    @classmethod
    def validate_config(cls, config: Any) -> Any:
        try:
            validate(config, cls.config_schema, format_checker=draft7_format_checker)
            return config
        except ValidationError as e:
            raise ConfigError(f"Config validation error: {e}")

    def create_task(self, example: Example) -> None:
        logger.debug(f"Creating {self.name} task for example_id={example.id}")
        # Assume all examples are images for a while
        self.client.create(
            path=f"/api/projects/{self.config['project_id']}/import",  # NB! no slash at the end
            data={
                "image": example.get_display_image(),
                self.token_field: str(example.id),
            },
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
                "project": self.config["project_id"],
                "url": url,
                "send_payload": True,
                "send_for_all_actions": False,
                "actions": list(self.event_map.keys()),
            },
        )

    def get_label(self, data: Any) -> Optional[str]:
        try:
            return data["annotation"]["result"][0]["value"]["choices"][0]
        except (TypeError, ValueError, KeyError) as e:
            logger.debug(f"No label found in Label Studio webhook: {e}")

    def receive_webhook(self, data: Any) -> None:
        try:
            example_id = IdOfExample(data["task"]["data"][self.token_field])
            example = Example.objects.get(id=example_id)
            action = self.event_map[data["action"]]
            result = {self.slug: data["annotation"], "label": self.get_label(data)}
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
        except (Example.DoesNotExist, MultipleObjectsReturned) as e:
            logger.error(
                f"{self.name} can't process received webhook request: {data}: {e}"
            )
