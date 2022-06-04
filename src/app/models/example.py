import logging
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

    project: models.ForeignKey = models.ForeignKey(
        "Project", null=False, blank=False, on_delete=models.CASCADE
    )
    status = models.IntegerField(choices=Status.choices, default=Status.pending)
    media_url: models.TextField = models.TextField(null=False, blank=False)
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.id)[:8]

    @classmethod
    def post_save(cls, sender, instance, created, *args, **kwargs):
        instance.project.updated_at = timezone.now()
        instance.project.save(update_fields=["updated_at"])
        if created:
            instance.project.start_workflow(instance.id)

    def set_started(self):
        self.status = Example.Status.started
        self.save(update_fields=["status"])
        ExampleEvent.objects.create(
            example=self,
            event_type=ExampleEvent.EventType.started,
        )

    def set_error(self, message):
        self.status = Example.Status.error
        self.save(update_fields=["status"])
        ExampleEvent.objects.create(
            example=self,
            event_type=ExampleEvent.EventType.error,
            properties={"message": message},
        )


post_save.connect(Example.post_save, sender=Example)


class ExampleAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "project", "status", "is_deleted")
    fields = (
        "id",
        "project",
        "status",
        "media_url",
        "properties",
        "created_at",
        "updated_at",
        "is_deleted",
    )


admin.site.register(Example, ExampleAdmin)
