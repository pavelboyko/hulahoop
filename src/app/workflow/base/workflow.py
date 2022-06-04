import logging
from uuid import UUID
from typing import Optional

logger = logging.getLogger(__package__)


class BaseWorkflow:
    """Base class for a project workflow"""

    project_id: Optional[UUID] = None

    def __init__(self, project_id: UUID):
        self.project_id = project_id
        logger.debug(f"BaseWorkflow initialized for project {project_id}")

    def start(self, example_id: UUID):
        pass
