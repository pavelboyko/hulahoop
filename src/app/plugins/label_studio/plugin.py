import logging
from typing import Optional, Dict, Any, Tuple
from uuid import UUID
from django.urls import reverse
from hulahoop.settings import HTTP_SCHEME, HOSTNAME
from app.plugins.base import BaseLabelingPlugin
from app.models import Example
from .client import LabelStudioClient

logger = logging.getLogger(__package__)


class LabelStudioPlugin(BaseLabelingPlugin):
    name: str = "Label Studio"
    slug: str = "labelstudio"

    client: LabelStudioClient

    def __init__(self, project_id: UUID, config: Dict[str, Any]):
        logger.debug(f"Initializing {self.name} plugin config={config}")
        self.client = LabelStudioClient(config)

        webhook_path = reverse("webhook_v1_0", args=[project_id, self.slug])
        webhook_url = f"{HTTP_SCHEME}{HOSTNAME}{webhook_path}"
        # As we init plugin in all celery workers on every start
        # make sure that our webhook wasn't already registered
        if not self.client.check_webhook_exists(webhook_url):
            logger.debug(f"Registering Label Studio webhook url={webhook_url}")
            self.client.create_webhook(webhook_url)

    def create_task(self, example: Example) -> None:
        # Assume all examples are images for a while
        self.client.create_image_labeling_task(example.id, example.media_url)

    def parse_result(
        self, data: Any
    ) -> Tuple[Optional[Example], Optional[BaseLabelingPlugin.Action], Any]:
        example_id = self.client.get_example_id_from_webhook_request(data)
        action = self.client.get_action_from_webhook_request(data)
        result = self.client.get_result_from_webhook_request(data)
        if not example_id:
            return None, action, result

        example = Example.objects.filter(id=example_id).last()
        return example, action, result
