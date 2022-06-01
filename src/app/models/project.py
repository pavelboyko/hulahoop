import logging
from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin
from .example import Example

logger = logging.getLogger(__package__)


class Project(BaseModel):
    """
    A container for examples, processing workflows, etc.
    """
    class MediaType(models.IntegerChoices):
        image = 0
        # video, audio, etc. will be here

    name: models.TextField = models.TextField()
    media_type: models.IntegerField = models.IntegerField(choices=MediaType.choices, default=MediaType.image)
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(
        "User", null=False, blank=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def start(self, example: Example) -> None:
        """
        Workflow entry point, executed immediately after an example was created
        """
        logger.debug(f"Project {self.name} started workflow for example {example}")


class ProjectAdmin(BaseAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("id", "name", "media_type", "created_by", "is_deleted")
    fields = (
        "id",
        "name",
        "media_type",
        "properties",
        "created_by",
        "created_at",
        "updated_at",
        "is_deleted",
    )
    search_fields = ("name",)

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        obj.save()


admin.site.register(Project, ProjectAdmin)
