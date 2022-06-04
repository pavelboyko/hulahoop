import logging
from uuid import UUID
from app.workflow.base import BaseWorkflow

logger = logging.getLogger(__package__)


class DemoWorkflow(BaseWorkflow):
    def __init__(self, project_id: UUID):
        super().__init__(project_id)
        logger.debug(f"DemoWorkflow initialized for project {project_id}")

    def start(self, example_id: UUID):
        logger.debug(
            f"DemoWorkflow started for project {self.project_id} example {example_id}"
        )
