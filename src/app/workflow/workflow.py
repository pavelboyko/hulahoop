import logging
from typing import Any
from app.workflow.base import BaseWorkflow
from app.plugins.base import BaseLabelingPlugin, ConfigError
from app.models import Example, ExampleEvent
from app.models.idof import IdOfProject, IdOfExample

logger = logging.getLogger(__package__)


class Workflow(BaseWorkflow):
    """The workflow"""

    labeling_plugin: BaseLabelingPlugin

    def __init__(self, project_id: IdOfProject, labeling_plugin: BaseLabelingPlugin):
        logger.debug(f"Initializing Workflow project_id={project_id}")
        super().__init__(project_id)
        self.labeling_plugin = labeling_plugin
        self.labeling_plugin.callback = self.on_labeling_event

    def start(self, example_id: IdOfExample):
        logger.debug(
            f"Starting Workflow project_id={self.project_id}, example_id={example_id}"
        )
        example = Example.objects.filter(id=example_id).last()
        if not example:
            logger.error(f"Can't find example by example_id={example_id}. Aborted.")
            return

        if self.labeling_plugin:
            try:
                self.labeling_plugin.create_task(example)
                example.set_labeling_started()
            except Exception as e:
                logger.error(
                    f"Error creating labeling task for example_id={example_id}: {e}"
                )
                example.set_labeling_error(str(e))

    def webhook(self, slug: str, data: Any):
        logger.debug(f"Workflow received some data: slug={slug}")

        if self.labeling_plugin and slug == self.labeling_plugin.slug:
            self.labeling_plugin.receive_callback(data)

    def on_labeling_event(
        self, example: Example, event: BaseLabelingPlugin.Event, result: Any
    ) -> None:
        if event == BaseLabelingPlugin.Event.annotation_created:
            example.set_labeling_completed(result)
        elif event == BaseLabelingPlugin.Event.annotation_updated:
            example.set_labeling_updated(result)
        elif event == BaseLabelingPlugin.Event.annotation_deleted:
            example.set_labeling_deleted()
