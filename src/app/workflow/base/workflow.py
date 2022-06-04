import logging
from uuid import UUID
from typing import Optional

logger = logging.getLogger(__package__)


class BaseWorkflow:
    """Base class for a project workflow"""

    project_id: Optional[UUID] = None
    initialized: bool = False

    def __init__(self, project_id: UUID):
        self.project_id = project_id

    def start(self, example_id: UUID):
        pass
