from django.contrib.auth.models import AbstractUser
from .base import BaseModel


class User(AbstractUser, BaseModel):
    pass
