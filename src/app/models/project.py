import logging
from django.db import models, transaction
from django.contrib import admin
from .base import BaseModel, BaseAdmin
from .idof import IdOfExample
from hulahoop.celery import app


logger = logging.getLogger(__package__)


class Project(BaseModel):
    """
    A container for examples, processing workflows, etc.
    """

    name: models.TextField = models.TextField()
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)
    created_by = models.ForeignKey(
        "User", null=False, blank=False, on_delete=models.CASCADE
    )
    is_archived: models.BooleanField = models.BooleanField(
        default=False, null=False, blank=False
    )

    def __str__(self):
        return self.name

    def example_count(self):
        return self.example_set.filter().count()  # type: ignore

    def issue_count(self):
        return self.issue_set.filter().count()  # type: ignore

    def start_workflow(self, example_id: IdOfExample) -> None:
        """Workflow entry point, executed after an example was created"""
        # transaction.on_commit is to make sure that example is saved
        # because we call start_workflow from an Example post_save signal
        # see https://stackoverflow.com/a/45279060
        transaction.on_commit(
            lambda: app.send_task("start_workflow", [self.pk, example_id])
        )

    def archive(self) -> None:
        self.is_archived = True
        self.save(update_fields=["is_archived"])

    def unarchive(self) -> None:
        self.is_archived = False
        self.save(update_fields=["is_archived"])


class ProjectAdmin(BaseAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = (
        "id",
        "name",
        "created_by",
    )
    fields = (
        "id",
        "name",
        "properties",
        "created_by",
        "created_at",
        "updated_at",
    )
    search_fields = ("name",)


admin.site.register(Project, ProjectAdmin)
