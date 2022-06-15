import logging
from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class ExampleTag(BaseModel):
    example: models.ForeignKey = models.ForeignKey(
        "Example", null=False, blank=False, on_delete=models.CASCADE
    )
    key: models.CharField = models.CharField(max_length=32)
    value: models.CharField = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.key}:{self.value}"


class ExampleTagAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "example",
        "key",
        "value",
    )
    fields = (
        "id",
        "example",
        "key",
        "value",
        "created_at",
        "updated_at",
    )


admin.site.register(ExampleTag, ExampleTagAdmin)
