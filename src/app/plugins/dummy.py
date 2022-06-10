import logging
from typing import Any
from app.models import Example
from app.models.idof import IdOfProject
from .base import BaseLabelingPlugin, ConfigError

logger = logging.getLogger(__package__)


class DummyLabelingPlugin(BaseLabelingPlugin):
    name: str = "Dummy Labeling"
    slug: str = "dummy_labeling"

    def __init__(self, project_id: IdOfProject, config: Any = None):
        super().__init__(project_id, config)
        logger.debug(f"Initializing {self.name} plugin config={config}")

    def create_task(self, example: Example) -> None:
        logger.debug(
            f"{self.name} is creating labeling task for example_id={example.id}"
        )
        example.set_labeling_started()
        logger.debug(
            f"Labeling started for example_id={example.id}, status={example.status}"
        )
        if self.callback:
            self.callback(example, BaseLabelingPlugin.Event.annotation_created, {})
            example.refresh_from_db()
            logger.debug(
                f"Labeling completed for example_id={example.id}, status={example.status}"
            )

    def receive_webhook(self, data: Any) -> None:
        logger.debug(f"{self.name} received some data on a webhook: {data}")
