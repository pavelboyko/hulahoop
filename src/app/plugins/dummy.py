import logging
from typing import Any
from app.models import Example
from app.models.idof import IdOfProject
from .base import BaseLabelingPlugin, ConfigError

logger = logging.getLogger(__package__)


class DummyLabelingPlugin(BaseLabelingPlugin):
    name: str = "Dummy Labeling"
    slug: str = "dummy_labeling"

    def __init__(self, project_id: IdOfProject, config: Any):
        logger.debug(f"Initializing {self.name} plugin config={config}")

    def create_task(self, example: Example) -> None:
        if self.callback:
            self.callback(example, BaseLabelingPlugin.Event.annotation_created, data={})
