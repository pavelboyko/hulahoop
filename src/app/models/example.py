from django.db import models
from django.contrib import admin
from app.models.base_model import BaseModel
from app.models.base_admin import BaseAdmin


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
        "uuid",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "workflow", "is_deleted")
    fields = (
        "id",
        "uuid",
        "workflow",
        "properties",
        "created_at",
        "updated_at",
        "is_deleted",
    )


admin.site.register(Example, ExampleAdmin)
