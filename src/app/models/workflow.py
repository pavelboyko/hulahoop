from django.db import models
from django.contrib import admin
from .base import BaseModel, BaseAdmin


class Workflow(BaseModel):
    """
    A repeatable example processing workflow.
    """

    name: models.TextField = models.TextField()
    properties: models.JSONField = models.JSONField(null=True, blank=True, default=None)
    created_by = models.ForeignKey("User", null=False, blank=False, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class WorkflowAdmin(BaseAdmin):
    readonly_fields = ("id", "created_at", "updated_at")
    list_display = ("id", "name", "created_by", "is_deleted")
    fields = (
        "id",
        "name",
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


admin.site.register(Workflow, WorkflowAdmin)
