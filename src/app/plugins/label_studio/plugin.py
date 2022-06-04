import logging
from typing import Optional, Dict, Any
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

        webhook_path = reverse('webhook_v1_0', args=[project_id, self.slug])
        webhook_url = f"{HTTP_SCHEME}{HOSTNAME}{webhook_path}"
        logger.debug(f"Registering Label Studio webhook url={webhook_url}")
        self.client.create_webhook(webhook_url)

    def create_labeling_task(self, example: Example) -> None:
        # Assume all examples are images for a while
        self.client.create_image_labeling_task(example.media_url)
