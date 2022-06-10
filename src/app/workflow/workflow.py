import logging
from typing import Any, Optional
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from app.workflow.base import BaseWorkflow
from app.plugins.base import BaseLabelingPlugin
from app.models import Example
from app.models.idof import IdOfProject, IdOfExample

logger = logging.getLogger(__package__)


class Workflow(BaseWorkflow):
    labeling_plugin: Optional[BaseLabelingPlugin] = None

    def __init__(
        self, project_id: IdOfProject, labeling_plugin: Optional[BaseLabelingPlugin]
    ):
        logger.debug(
            f"Initializing Workflow project_id={project_id} labeling_plugin={labeling_plugin}"
        )
        super().__init__(project_id)
        if labeling_plugin:
            self.labeling_plugin = labeling_plugin
            self.labeling_plugin.callback = self.on_labeling_event
            self.webhook_receivers.append(labeling_plugin)

    def start(self, example_id: IdOfExample):
        try:
            example = Example.objects.get(id=example_id)
            self.label_example(example)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            logger.error(
                f"Can't get a single example for example_id={example_id}: {e}. Aborted."
            )

    def label_example(self, example: Example) -> None:
        if not self.labeling_plugin:
            return

        try:
            example.set_labeling_started()
            self.labeling_plugin.create_task(example)
        except Exception as e:
            logger.error(f"Error creating labeling task for example={example}: {e}")
            if example:
                example.set_labeling_error(str(e))

    def on_labeling_event(
        self, example: Example, event: BaseLabelingPlugin.Event, result: Any
    ) -> None:
        match event:
            case BaseLabelingPlugin.Event.annotation_created:
                example.set_labeling_completed(result)
            case BaseLabelingPlugin.Event.annotation_updated:
                example.set_labeling_updated(result)
            case BaseLabelingPlugin.Event.annotation_deleted:
                example.set_labeling_deleted()
