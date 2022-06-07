from django.db import models
from django.contrib import admin
from prettyjson import PrettyJSONWidget


class BaseModel(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, null=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": PrettyJSONWidget(attrs={"initial": "parsed"})}
    }
