from django.contrib import admin
from prettyjson import PrettyJSONWidget
from django.db.models import JSONField


class BaseAdmin(admin.ModelAdmin):
    formfield_overrides = {
        JSONField: {"widget": PrettyJSONWidget(attrs={"initial": "parsed"})}
    }
