import logging
from django.db import models
from django.db.models.signals import post_save
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class Example(BaseModel):
    """
    A single ML example
    """

    workflow: models.ForeignKey = models.ForeignKey(
        "Workflow", null=False, blank=False, on_delete=models.CASCADE
    )
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.id)

    @classmethod
    def post_create(cls, sender, instance, created, *args, **kwargs):
        if created:
            instance.workflow.start(instance)


post_save.connect(Example.post_create, sender=Example)


class ExampleAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "workflow", "is_deleted")
    fields = (
        "id",
        "workflow",
        "properties",
        "created_at",
        "updated_at",
        "is_deleted",
    )


admin.site.register(Example, ExampleAdmin)
