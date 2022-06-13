import logging
from typing import Any
import uuid
from django.utils import timezone
from django.db import models
from django.db.models.signals import post_save
from django.contrib import admin
from .base import BaseModel, BaseAdmin
from .example_event import ExampleEvent

logger = logging.getLogger(__package__)


class Example(BaseModel):
    """
    A single ML example
    """

    class Status(models.IntegerChoices):
        pending = 0
        skipped = 10
        started = 20
        completed = 30
        canceled = 40
        error = 50

    # Use UUID pk to allow client-side ID allocation
    id: models.UUIDField = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    project: models.ForeignKey = models.ForeignKey(
        "Project", null=False, blank=False, on_delete=models.CASCADE
    )
    status = models.IntegerField(choices=Status.choices, default=Status.pending)
    media_url: models.TextField = models.TextField(null=False, blank=False)
    fingerprint: models.TextField = models.TextField(
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

    def set_labeling_started(self):
        self.status = Example.Status.started
        self.save(update_fields=["status"])
        ExampleEvent.objects.create(
            example=self,
            event_type=ExampleEvent.EventType.labeling_started,
        )

    def set_labeling_error(self, message):
        self.status = Example.Status.error
        self.save(update_fields=["status"])
        ExampleEvent.objects.create(
            example=self,
            event_type=ExampleEvent.EventType.labeling_error,
            properties={"message": message},
        )

    def set_labeling_completed(self, result: Any):
        self.status = Example.Status.completed
        self.save(update_fields=["status"])
        ExampleEvent.objects.create(
            example=self,
            event_type=ExampleEvent.EventType.labeling_completed,
            properties={"result": result},
        )

    def set_labeling_updated(self, result: Any):
        # do not change status
        ExampleEvent.objects.create(
            example=self,
            event_type=ExampleEvent.EventType.labeling_updated,
            properties={"result": result},
        )

    def set_labeling_deleted(self):
        self.status = Example.Status.started
        self.save(update_fields=["status"])
        ExampleEvent.objects.create(
            example=self,
            event_type=ExampleEvent.EventType.labeling_deleted,
        )


post_save.connect(Example.post_save, sender=Example)


class ExampleAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "project", "issue", "status")
    fields = (
        "id",
        "project",
        "issue",
        "status",
        "media_url",
        "fingerprint",
        "properties",
        "created_at",
        "updated_at",
    )


admin.site.register(Example, ExampleAdmin)
