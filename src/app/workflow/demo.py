import logging
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
                {
                    "LABELSTUDIO_URL": "http://host.docker.internal:8080/",
                    "LABELSTUDIO_API_KEY": "d3bca97b95da0820cadae2197c7ccde4ee6e77b7",
                    "LABELSTUDIO_PROJECT_ID": 2,
                }
            )
        except ConfigError as error:
            logger.error(f"Label Studio configuration error: {error}. Workflow initialization aborted.")
            return

        self.initialized = True

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
            self.labeling_plugin.create_labeling_task(example)

            example.status = Example.Status.started
            example.save(update_fields=["status"])
            ExampleEvent.objects.create(
                example_id=example_id, event_type=ExampleEvent.EventType.started
            )
        except RestRequestError as e:
            example.status = Example.Status.error
            example.save(update_fields=["status"])
            ExampleEvent.objects.create(
                example_id=example_id, event_type=ExampleEvent.EventType.error, properties={"message": e.message}
            )



