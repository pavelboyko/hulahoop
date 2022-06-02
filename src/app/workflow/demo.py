"""
This is a demo workflow, to be better understood and generalized later on
"""
import logging
import uuid

import app.models.example
from app.models.example_event import ExampleEvent
import app.integrations.label_studio as ls

logger = logging.getLogger(__package__)


def start(project_id: uuid.UUID, example_id: uuid.UUID) -> None:
    logger.debug(
        f"Started demo workflow for project {project_id} / example {example_id}"
    )
    # TODO: check that project media_type is image
    create_labeling_task(project_id, example_id)


def create_labeling_task(project_id: uuid.UUID, example_id: uuid.UUID) -> None:
    # TODO: replace me by project-level Label Studio plugin configuration
    LABELSTUDIO_URL = "http://host.docker.internal:8080/"
    LABELSTUDIO_API_KEY = "d3bca97b95da0820cadae2197c7ccde4ee6e77b"
    LABELSTUDIO_PROJECT_ID = "2"

    media_urls = app.models.example.Example.objects.filter(id=example_id).values_list(
        "media_url", flat=True
    )
    if not media_urls or len(media_urls) != 1:
        logger.error(
            f"create_labeling_task: Can't find example id = {example_id}, skipped"
        )
        return

    success, message = ls.create_image_labeling_task(
        LABELSTUDIO_URL, LABELSTUDIO_API_KEY, LABELSTUDIO_PROJECT_ID, media_urls[0]
    )
    if success:
        app.models.Example.objects.filter(id=example_id).update(
            status=app.models.Example.Status.started
        )
        ExampleEvent.objects.create(
            example_id=example_id, event_type=ExampleEvent.EventType.started
        )
    else:
        app.models.Example.objects.filter(id=example_id).update(
            status=app.models.Example.Status.error
        )
        ExampleEvent.objects.create(
            example_id=example_id,
            event_type=ExampleEvent.EventType.error,
            properties={"message": message},
        )
