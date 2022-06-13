import logging
from typing import Dict, Any
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from app.models import Project
from app.models.idof import IdOfProject, IdOfExample
from app.plugins import BaseLabelingPlugin, build_labeling_plugin
from .base import BaseWorkflow
from .workflow import Workflow

logger = logging.getLogger(__package__)

# The global per project workflow registry
# The registry is local to the celery worker, this means
# that every workflow must be initialized in every worker
project_workflow: Dict[IdOfProject, BaseWorkflow] = {}


def build(project_id: IdOfProject) -> None:
    try:
        props = Project.objects.get(id=project_id).properties
        labeling_plugin = None
        if props is not None and "plugins" in props:
            if "labeling" in props["plugins"]:
                labeling_plugin = build_labeling_plugin(
                    project_id,
                    props["plugins"]["labeling"]["slug"],
                    props["plugins"]["labeling"]["config"],
                )
        else:
            logger.warning(
                f"For project_id {project_id} 'plugins' sections is not found in properties, check configuration."
            )
        project_workflow[project_id] = Workflow(project_id, labeling_plugin)
    except Exception as e:
        logger.error(
            f"Problem during project initialization: project_id={project_id}, error={e}. Aborted."
        )


def rebuild(project_id: IdOfProject) -> None:
    if project_id in project_workflow:
        del project_workflow[project_id]
    build(project_id)


def get_workflow(project_id: IdOfProject) -> BaseWorkflow:
    if project_id not in project_workflow:
        build(project_id)

    return project_workflow.get(project_id)


def start(project_id: IdOfProject, example_id: IdOfExample):
    """Start workflow for a specific project and example
    This function is executed by a celery worker (see tasks.py)
    """

    get_workflow(project_id).start(example_id)


def webhook(project_id: IdOfProject, slug: str, data: Any):
    """Handle data received to webhook
    This function is executed by a celery worker (see tasks.py)
    """

    get_workflow(project_id).webhook(slug, data)
