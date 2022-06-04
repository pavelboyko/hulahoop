import logging
from typing import Dict, Any
from uuid import UUID
from app.workflow.base import BaseWorkflow
from .demo import DemoWorkflow

logger = logging.getLogger(__package__)

# The global per project workflow registry
# TODO: provide a method to re-initialize workflow if project settings changed
__registry: Dict[UUID, BaseWorkflow] = {}


def start(project_id: UUID, example_id: UUID):
    """Start workflow for a specific project and example
    This function is supposed to be executed by a celery worket (see tasks.py)
    A call chain is supposed to be: this function -> Workflow -> Plugin(s) -> Client (see plugins/base/)
    """

    if project_id not in __registry:
        # Initialize workflow at first start() call
        # In the future we will customize workflow depending on project settings
        # But for now the one and the only DemoWorkflow is hardcoded here
        __registry[project_id] = DemoWorkflow(project_id)

    __registry[project_id].start(example_id)


def webhook(project_id: UUID, slug: str, data: Any):
    """Handle data received to webhook
    This function is supposed to be executed by a celery worket (see tasks.py)
    A call chain is supposed to be: this function -> Workflow -> Plugin(s) -> Workflow
    """
    if project_id not in __registry:
        # See comment above
        __registry[project_id] = DemoWorkflow(project_id)

    __registry[project_id].webhook(slug, data)
