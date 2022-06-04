"""
This is a demo workflow, to be better understood and generalized later on
"""
from typing import Dict
import logging
from uuid import UUID

from app.models import Example, ExampleEvent, Project
from app.plugins import label_studio

logger = logging.getLogger(__package__)

initialized: Dict[UUID, bool] = {}

"""
TODO на свежую голову -- Workflow должно само инициализировать нужные плагины
один раз для каждого проекта при первом вызове (?) и при изменениях в конфигурации
плагинов и самого Workflow.

Может быть состояние инициализации стоит хранить в БД, но это не точно. Plugin manager
и запуск чего-то после инициализации Django не нужны, достаточно иметь все
в workflow и запускать при первом start. Настройки плагинов держать внутри проекта и
внутри организации (похоже нужна такая модель и связь между проектами и организациями
чтобы не настраивать каждый плагин заново для каждого проекта).

Может быть тут в словаре initialized нужно держать не bool, а, собственно, 
инициализированные объекты workflow для каждого проекта, а в них держать 
инициализированные объекты plugin для каждого нужного плагина. При любых изменениях
настроек можно будет просто удалять и заново создавать запись, попутно ловить ошибки
если какой-то плагин не хочет работать.
"""


def init(project_id: UUID) -> None:
    global initialized

    logger.debug("Initializing demo workflow...")


def start(project_id: UUID, example_id: UUID) -> None:
    if project_id not in initialized:
        init(project_id)

    create_labeling_task(project_id, example_id)


def create_labeling_task(project_id: UUID, example_id: UUID) -> None:
    LABELSTUDIO_PROJECT_ID = 2

    media_urls = Example.objects.filter(id=example_id).values_list(
        "media_url", flat=True
    )
    if not media_urls or len(media_urls) != 1:
        logger.error(
            f"create_labeling_task: Can't find example id = {example_id}, skipped"
        )
        return

    success, message = label_studio.create_image_labeling_task(
        LABELSTUDIO_PROJECT_ID, media_urls[0]
    )
    if success:
        Example.objects.filter(id=example_id).update(status=Example.Status.started)
        ExampleEvent.objects.create(
            example_id=example_id, event_type=ExampleEvent.EventType.started
        )
    else:
        Example.objects.filter(id=example_id).update(status=Example.Status.error)
        ExampleEvent.objects.create(
            example_id=example_id,
            event_type=ExampleEvent.EventType.error,
            properties={"message": message},
        )
