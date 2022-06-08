from typing import Dict, Any
from app.models.idof import IdOfProject, IdOfExample
from app.workflow.base import BaseWorkflow
from app.plugins.label_studio import LabelStudioPlugin
from .workflow import Workflow

# The global per project workflow registry
# XXX: the registry is local to the celery worker
# This means that every workflow must be initialized in every worker
project_workflow: Dict[IdOfProject, BaseWorkflow] = {}


def build(project_id: IdOfProject) -> None:
    # In the (near) future we will take labeling plugin type and configuration from project config
    # For now just hardcode Labeling Studio config here
    labeling_plugin = LabelStudioPlugin(
        project_id,
        {
            "LABELSTUDIO_URL": "http://host.docker.internal:8080/",
            "LABELSTUDIO_API_KEY": "d3bca97b95da0820cadae2197c7ccde4ee6e77b7",
            "LABELSTUDIO_PROJECT_ID": 2,
        },
    )
    # FIXME: catch ConfigError, RestClient.RequestError

    project_workflow[project_id] = Workflow(project_id, labeling_plugin)


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
