from enum import Enum
import logging
from django.db import models
from django.db.models.signals import post_save
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class ExampleStatus(Enum):
    pending = 0
    skipped = 10
    started = 20
    completed = 30
    canceled = 40
    error = 50


class Example(BaseModel):
    """
    A single ML example
    """

    project: models.ForeignKey = models.ForeignKey(
        "Project", null=False, blank=False, on_delete=models.CASCADE
    )
    status = models.IntegerField(
        choices=[(tag.value, tag.name) for tag in ExampleStatus],
        default=ExampleStatus.pending.value,
    )
    media_url: models.TextField = models.TextField(null=False, blank=False)
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.id)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            instance.project.start(instance)


post_save.connect(Example.post_create, sender=Example)


class ExampleAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "project", "status", "is_deleted")
    fields = (
        "id",
        "project",
        "status",
        "media_url",
        "properties",
        "created_at",
        "updated_at",
        "is_deleted",
    )


admin.site.register(Example, ExampleAdmin)
