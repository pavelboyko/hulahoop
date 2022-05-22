import uuid
from django.db import models


class BaseModel(models.Model):
    uuid: models.UUIDField = models.UUIDField(
        unique=True, default=uuid.uuid4, editable=False
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, null=True
    )
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, null=True)
    is_deleted: models.BooleanField = models.BooleanField(default=False)

    class Meta:
        abstract = True
