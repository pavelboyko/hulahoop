import logging
from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class ExampleEvent(BaseModel):
    """
    An example processing event, e.g. "Labeling started", "Labeling completed", "Error", etc.
    """

    class EventType(models.IntegerChoices):
        default = 0
        labeling_started = 10
        labeling_completed = 20
        labeling_error = 30
        labeling_updated = 40
        labeling_deleted = 50

    example: models.ForeignKey = models.ForeignKey(
        "Example", null=False, blank=False, on_delete=models.CASCADE
    )
    event_type: models.IntegerField = models.IntegerField(
        choices=EventType.choices, default=EventType.default
    )
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.id)[:8]


class ExampleEventAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "example", "event_type")
    fields = (
        "id",
        "example",
        "event_type",
        "properties",
        "created_at",
        "updated_at",
        "is_deleted",
    )


admin.site.register(ExampleEvent, ExampleEventAdmin)
