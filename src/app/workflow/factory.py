import logging
from typing import Dict, Any
from uuid import UUID
from app.workflow.base import BaseWorkflow
from .demo import DemoWorkflow

logger = logging.getLogger(__package__)

# The global per project workflow registry
# XXX: the register is local to the celery worker
# This means that every workflow must be initialized in every worker
__registry: Dict[UUID, BaseWorkflow] = {}


def build(project_id: UUID) -> None:
    """Initialize workflow for a project
    In the future we will customize workflow depending on project settings
    But for now the one and the only DemoWorkflow is hardcoded here
    """
    __registry[project_id] = DemoWorkflow(project_id)


def start(project_id: UUID, example_id: UUID):
    """Start workflow for a specific project and example
    This function is supposed to be executed by a celery worker (see tasks.py)

    A call chain is supposed to be:
        this function
        -> Workflow to execute some actions
            -> Plugin to interface with 3rd party service
                -> Client to do requests
    """

    if project_id not in __registry:
        build(project_id)

    __registry[project_id].start(example_id)


def webhook(project_id: UUID, slug: str, data: Any):
    """Handle data received to webhook
    This function is supposed to be executed by a celery worker (see tasks.py)

    A call chain is supposed to be:
        this function
        -> Workflow to route data to relevant plugin
            -> Plugin to interpret data
                -> Client to decode data transport format
            -> Plugin to return decoded data to Workflow
        -> Workflow to take some actions depending on the data received
    """
    if project_id not in __registry:
        build(project_id)

    __registry[project_id].webhook(slug, data)
