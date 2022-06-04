import logging
from typing import Optional, Dict, Any
from uuid import UUID
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
        webhook_slug = f"{self.slug}-{str(project_id)}"
        self.client = LabelStudioClient(config, webhook_slug)

    def create_labeling_task(self, example: Example) -> None:
        # Assume all examples are images for a while
        self.client.create_image_labeling_task(example.media_url)
