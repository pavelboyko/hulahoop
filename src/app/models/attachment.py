import logging
from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class Attachment(BaseModel):
    class Type(models.IntegerChoices):
        unknown = 0
        image = 1
        video = 2
        audio = 3
        text = 4

    example: models.ForeignKey = models.ForeignKey(
        "Example", null=False, blank=False, on_delete=models.CASCADE
    )
    url: models.TextField = models.TextField()
    type: models.IntegerField = models.IntegerField(
        choices=Type.choices, default=Type.unknown
    )

    def __str__(self):
        return self.url


class AttachmentAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "example",
        "url",
        "type",
    )
    fields = (
        "id",
        "example",
        "url",
        "type",
        "created_at",
        "updated_at",
    )


admin.site.register(Attachment, AttachmentAdmin)
