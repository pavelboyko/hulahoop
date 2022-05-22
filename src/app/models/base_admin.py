from django.contrib import admin
from prettyjson import PrettyJSONWidget

# from django.contrib.postgres.fields import JSONField


class BaseAdmin(admin.ModelAdmin):
    pass


#    formfield_overrides = {
#        JSONField: {"widget": PrettyJSONWidget(attrs={"initial": "parsed"})}
#    }
