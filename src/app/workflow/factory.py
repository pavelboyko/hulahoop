import logging
from typing import Dict
from uuid import UUID
from app.workflow.base import BaseWorkflow
from .demo import DemoWorkflow

logger = logging.getLogger(__package__)

# The global per project workflow registry
# TODO: provide a method to re-initialize workflow if project settings changed
__registry: Dict[UUID, BaseWorkflow] = {}


def start(project_id: UUID, example_id: UUID):
    """Start workflow for a specific project and example
    A normal call chain is supposed to be: this function -> Workflow -> Plugin(s) -> Client (see plugins/base/)
    """

    if project_id not in __registry:
        # Initialize workflow at first start() call
        # In the future we will customize workflow depending on project settings
        # But for now the one and the only DemoWorkflow is hardcoded here
        __registry[project_id] = DemoWorkflow(project_id)

    __registry[project_id].start(example_id)
