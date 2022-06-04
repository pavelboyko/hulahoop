import logging
from uuid import UUID
from typing import Optional, Any

logger = logging.getLogger(__package__)


class BaseWorkflow:
    """Base class for a project workflow"""

    project_id: Optional[UUID] = None
    initialized: bool = False

    def __init__(self, project_id: UUID):
        self.project_id = project_id

    def start(self, example_id: UUID):
        """Executed when new example is added to the project"""
        pass

    def webhook(self, slug: str, data: Any):
        """Executed when the webhook API endpoint receives data for the project"""
        pass
