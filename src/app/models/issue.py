import logging
from django.utils import timezone
from django.db import models
from django.contrib import admin

from app.models.example import Example
from .base import BaseModel, BaseAdmin
from .tag import Tag

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
    name: models.TextField = models.TextField(null=True, blank=True, db_index=True)
    fingerprint: models.TextField = models.TextField(
        null=True, blank=True, default=None, db_index=True
    )
    first_seen: models.DateTimeField = models.DateTimeField(
        default=timezone.now,
        null=True,
    )
    last_seen: models.DateTimeField = models.DateTimeField(
        default=timezone.now,
        null=True,
    )

    def __str__(self) -> str:
        return f"#{self.id}"  # type: ignore

    def add_example(self, example: Example) -> None:
        example.issue = self
        example.save(update_fields=["issue"])
        if example.created_at < self.first_seen:
            self.first_seen = example.created_at
            self.save(update_fields=["first_seen"])
        if example.created_at > self.last_seen:
            self.last_seen = example.created_at
            self.save(update_fields=["last_seen"])
        # TODO: reopen resolved issue here?


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
        "created_at",
        "updated_at",
    )


admin.site.register(Issue, IssueAdmin)
