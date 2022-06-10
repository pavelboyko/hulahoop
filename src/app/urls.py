from django.urls import path
from django.conf.urls import include
from app import api
from app.models.idof import IdOfProjectPathConverter


urlpatterns = [
    path(
        f"capture/<{IdOfProjectPathConverter}:project_id>/",
        api.capture,
        name="api_capture",
    ),
    path(
        f"webhook/<{IdOfProjectPathConverter}:project_id>/<slug:slug>/",
        api.webhook,
        name="api_webhook",
    ),
]
