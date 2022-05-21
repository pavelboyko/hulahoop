from django.db import models
#from django.contrib.postgres.fields import JSONField
from django.contrib import admin
from app.models.base_model import BaseModel
from app.models.base_admin import BaseAdmin


class Loop(BaseModel):
    """
    A loop is a repeatable example processing workflow.
    """

    name: models.TextField = models.TextField()
#    properties: JSONField = JSONField(null=True, blank=True, default=None)

    def __str__(self):
        return self.name


class LoopAdmin(BaseAdmin):
    readonly_fields = ("id", "uuid", "created_at", "updated_at")
    list_display = ("id", "name", "is_deleted")
    fields = (
        "id",
        "uuid",
        "name",
        "created_at",
        "updated_at",
        "is_deleted",
    )
    search_fields = ("name",)


admin.site.register(Loop, LoopAdmin)
