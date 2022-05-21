from django.db import models
#from django.contrib.postgres.fields import JSONField
from django.contrib import admin
from app.models.base_model import BaseModel
from app.models.base_admin import BaseAdmin


class Example(BaseModel):
    """
    A single ML example
    """

    loop: models.ForeignKey = models.ForeignKey(
        "Loop", null=False, blank=False, on_delete=models.CASCADE
    )
#    properties: JSONField = JSONField(null=True, blank=True, default=None)


class ExampleAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "uuid",
        "created_at",
        "updated_at",
    )
    list_display = ("id", "loop", "is_deleted")
    fields = (
        "id",
        "uuid",
        "loop",
        "created_at",
        "updated_at",
        "is_deleted",
    )


admin.site.register(Example, ExampleAdmin)
