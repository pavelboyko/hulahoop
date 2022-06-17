import logging
from typing import Any, Optional
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from app.workflow.base import BaseWorkflow
from app.plugins.base import BaseLabelingPlugin
from app.models import Example, Issue
from app.models.idof import IdOfProject, IdOfExample
from app.grouping import get_or_create_issue

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
            self.group_example(example)
            self.label_example(example)
        except (ObjectDoesNotExist, MultipleObjectsReturned) as e:
            logger.error(
                f"Can't get a single example for example_id={example_id}: {e}. Aborted."
            )

    def group_example(self, example: Example) -> Optional[Issue]:
        logger.debug("Grouping example {example}")
        issue, is_created = get_or_create_issue(example)
        example.refresh_from_db()
        logger.debug(f"issue={issue}, is_created={is_created}")
        return issue

    def label_example(self, example: Example) -> None:
        if not self.labeling_plugin:
            return

        try:
            self.labeling_plugin.create_task(example)
        except Exception as e:
            logger.error(f"Error creating labeling task for example={example}: {e}")

    def on_labeling_event(
        self, example: Example, event: BaseLabelingPlugin.Event, result: Any
    ) -> None:
        # TODO: save or update annotation results, we will return to this when we better undertand annotations data structure
        pass
