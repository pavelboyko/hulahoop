from typing import Any, Callable, Optional
from enum import Enum
from app.models.idof import IdOfProject
from app.models import Example


class ConfigError(Exception):
    """Raised on errors in plugin configuration"""

    pass


class BasePlugin:
    name: str = ""
    slug: str = ""

    def receive_webhook(self, data: Any) -> None:
        pass


class BaseLabelingPlugin(BasePlugin):
    class Event(Enum):
        annotation_created = 0
        annotation_updated = 1
        annotation_deleted = 2
        # add more event types here if needed

    # called when labeling service returns an event related to specific Example
    callback: Optional[Callable[[Example, Event, Any], None]] = None

    def __init__(self, project_id: IdOfProject, config: Any):
        pass

    def create_task(self, example: Example) -> None:
        pass
