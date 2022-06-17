import logging
from typing import Any
import uuid
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib import admin
from .base import BaseModel, BaseAdmin

logger = logging.getLogger(__package__)


class Example(BaseModel):
    """
    A single ML example
    """

    # Use UUID pk to allow client-side ID allocation
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    project: models.ForeignKey = models.ForeignKey(
        "Project", null=False, blank=False, on_delete=models.CASCADE
    )
    media_url: models.TextField = models.TextField(null=False, blank=False)
    fingerprint: models.TextField = models.TextField(
        null=True, blank=True, default=None
    )
    predictions: models.JSONField = models.JSONField(
        null=True, blank=True, default=None
    )
    annotations: models.JSONField = models.JSONField(
        null=True, blank=True, default=None
    )
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)
    issue: models.ForeignKey = models.ForeignKey(
        "Issue", null=True, blank=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.id)[:8]

    @classmethod
    def post_save(cls, sender, instance, created, *args, **kwargs):
        instance.project.updated_at = timezone.now()
        instance.project.save(update_fields=["updated_at"])
        if instance.issue:
            instance.issue.updated_at = timezone.now()
            instance.issue.save(update_fields=["updated_at"])
        if created:
            instance.project.start_workflow(instance.id)


post_save.connect(Example.post_save, sender=Example)


class ExampleAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "project", "issue")
    fields = (
        "id",
        "project",
        "issue",
        "media_url",
        "fingerprint",
        "predictions",
        "annotations",
        "properties",
        "created_at",
        "updated_at",
    )


admin.site.register(Example, ExampleAdmin)
