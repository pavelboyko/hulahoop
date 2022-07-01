import logging
from typing import Dict, Any
from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class Tag(BaseModel):
    key_max_length: int = 30
    value_max_length: int = 200

    example: models.ForeignKey = models.ForeignKey(
        "Example", null=False, blank=False, on_delete=models.CASCADE
    )
    key: models.CharField = models.CharField(max_length=key_max_length, db_index=True)
    value: models.CharField = models.CharField(
        max_length=value_max_length, db_index=True
    )

    def __str__(self):
        return f"{self.key}:{self.value}"


class TagAdmin(BaseAdmin):
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


admin.site.register(Tag, TagAdmin)
