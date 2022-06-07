import logging
from typing import Dict, Any
from app.models.idof import IdOfProject, IdOfExample
from app.workflow.base import BaseWorkflow
from .demo import DemoWorkflow

logger = logging.getLogger(__package__)

# The global per project workflow registry
# XXX: the register is local to the celery worker
# This means that every workflow must be initialized in every worker
__registry: Dict[IdOfProject, BaseWorkflow] = {}


def build(project_id: IdOfProject) -> None:
    """Initialize workflow for a project
    But for now the one and the only DemoWorkflow is hardcoded here
    """
    __registry[project_id] = DemoWorkflow(project_id)


def start(project_id: IdOfProject, example_id: IdOfExample):
    """Start workflow for a specific project and example
    This function is executed by a celery worker (see tasks.py)
    """

    if project_id not in __registry:
        build(project_id)

    __registry[project_id].start(example_id)


def webhook(project_id: IdOfProject, slug: str, data: Any):
    """Handle data received to webhook
    This function is executed by a celery worker (see tasks.py)
    """
    if project_id not in __registry:
        build(project_id)

    __registry[project_id].webhook(slug, data)
