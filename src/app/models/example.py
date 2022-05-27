from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin


class Example(BaseModel):
    """
    A single ML example
    """

    workflow: models.ForeignKey = models.ForeignKey(
        "Workflow", null=False, blank=False, on_delete=models.CASCADE
    )
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)


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
