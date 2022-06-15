import logging
from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class Issue(BaseModel):
    """
    A group of similar Examples
    """

    class Status(models.IntegerChoices):
        open = 0
        muted = 10
        resolved = 20  # a resolved Issue can receive new Examples and reopen
        closed = 30  # a closed Issue can not receive new Examples

    project: models.ForeignKey = models.ForeignKey(
        "Project", null=False, blank=False, on_delete=models.CASCADE
    )
    status: models.IntegerField = models.IntegerField(
        choices=Status.choices, default=Status.open
    )
    name: models.TextField = models.TextField(null=True, blank=True)
    fingerprint: models.TextField = models.TextField(
        null=True, blank=True, default=None
    )
    tags: models.JSONField = models.JSONField(null=True, blank=True, default=None)

    def __str__(self) -> str:
        return f"#{self.id}"

    def example_count(self) -> int:
        return self.example_set.filter().count()


class IssueAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "project",
        "name",
        "status",
    )
    fields = (
        "id",
        "project",
        "name",
        "status",
        "tags",
        "created_at",
        "updated_at",
    )


admin.site.register(Issue, IssueAdmin)
