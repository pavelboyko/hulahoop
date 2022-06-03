import logging
import uuid
from django.db import models, transaction
from django.contrib import admin
from .base import BaseModel, BaseAdmin
from hulahoop.celery import app


logger = logging.getLogger(__package__)


class Project(BaseModel):
    """
    A container for examples, processing workflows, etc.
    """

    class MediaType(models.IntegerChoices):
        image = 0
        # video, audio, etc. will be here

    name: models.TextField = models.TextField()
    media_type: models.IntegerField = models.IntegerField(
        choices=MediaType.choices, default=MediaType.image
    )
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(
        "User", null=False, blank=False, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    def example_count(self):
        return self.example_set.all().count()

    def start_workflow(self, example_id: uuid.UUID) -> None:
        """Workflow entry point, executed after an example was created"""
        # transaction.on_commit is to make sure that example is saved
        # because we call start_workflow from an Example post_save signal
        # see https://stackoverflow.com/a/45279060
        transaction.on_commit(
            lambda: app.send_task("start_workflow", [self.id, example_id])
        )


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
