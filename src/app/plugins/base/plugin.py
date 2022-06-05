from typing import Tuple, Optional, Any
from enum import Enum
from app.models import Example


class BasePlugin:
    name: str = ""
    slug: str = ""


class BaseLabelingPlugin(BasePlugin):
    class Action(Enum):
        ANNOTATION_CREATED = (0,)
        ANNOTATION_UPDATED = (1,)
        ANNOTATION_DELETED = (2,)

    def create_task(self, example: Example) -> None:
        pass

    def parse_result(
        self, data: Any
    ) -> Tuple[Optional[Example], Optional[Action], Any]:
        """
        :return: Tuple (example ID, action, result)
        """
        pass
