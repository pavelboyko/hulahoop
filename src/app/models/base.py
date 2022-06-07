from django.db import models
from django.utils import timezone
from django.contrib import admin
from prettyjson import PrettyJSONWidget


class BaseModel(models.Model):
    created_at: models.DateTimeField = models.DateTimeField(
        # we do not use auto_now_add=True here to be able to overwrite created_at in tests
        # see https://github.com/FactoryBoy/factory_boy/issues/102#issuecomment-28010862
        default=timezone.now,
        null=True,
    )
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {"widget": PrettyJSONWidget(attrs={"initial": "parsed"})}
    }
