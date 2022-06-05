import logging
from typing import Any
from uuid import UUID
from app.workflow.base import BaseWorkflow
from app.plugins.base import BaseLabelingPlugin, ConfigError, RestRequestError
from app.plugins.label_studio import LabelStudioPlugin
from app.models import Example, ExampleEvent

logger = logging.getLogger(__package__)


class DemoWorkflow(BaseWorkflow):
    """The workflow"""

    labeling_plugin: BaseLabelingPlugin

    def __init__(self, project_id: UUID):
        logger.debug(f"Initializing DemoWorkflow project_id={project_id}")
        super().__init__(project_id)

        # In the future we will take labeling plugin type and configuration from project config
        # For now just hardcode Labeling Studio config here
        try:
            self.labeling_plugin = LabelStudioPlugin(
                project_id,
                {
                    "LABELSTUDIO_URL": "http://host.docker.internal:8080/",
                    "LABELSTUDIO_API_KEY": "d3bca97b95da0820cadae2197c7ccde4ee6e77b7",
                    "LABELSTUDIO_PROJECT_ID": 2,
                },
            )
            self.initialized = True
        except ConfigError as e:
            logger.error(
                f"Label Studio configuration error: {e}. Workflow initialization aborted."
            )
        except RestRequestError as e:
            logger.error(
                f"Label Studio API request error: {e}. Workflow initialization aborted."
            )

    def start(self, example_id: UUID):
        logger.debug(
            f"Starting DemoWorkflow project_id={self.project_id}, example_id={example_id}"
        )
        if not self.initialized:
            logger.debug("DemoWorkflow is not properly initialized. Aborted.")
            return

        example = Example.objects.filter(id=example_id).last()
        if not example:
            logger.error(f"Can't find example by example_id={example_id}. Aborted.")
            return

        try:
            self.labeling_plugin.create_task(example)
            example.set_labeling_started()
        except RestRequestError as e:
            example.set_labeling_error(str(e))

    def webhook(self, slug: str, data: Any):
        logger.debug(f"DemoWorkflow received some data: slug={slug}")
        if not self.initialized:
            logger.debug("DemoWorkflow is not properly initialized. Aborted.")
            return

        if slug == self.labeling_plugin.slug:
            example, action, result = self.labeling_plugin.parse_result(data)
            if not example or not action:
                logger.warning(
                    f"Label Studio plugin wasn't able to parse example_id or action from webhook data {data}. Ignoring."
                )
                return

            if action == BaseLabelingPlugin.Action.ANNOTATION_CREATED:
                example.set_labeling_completed()
            elif action == BaseLabelingPlugin.Action.ANNOTATION_UPDATED:
                example.set_labeling_updated()
            elif action == BaseLabelingPlugin.Action.ANNOTATION_DELETED:
                example.set_labeling_deleted()
