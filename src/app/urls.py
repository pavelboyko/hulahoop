from django.urls import path
from django.conf.urls import include
from app import api

urlpatterns = [
    path("capture/<int:project_id>/", api.capture, name="api_capture"),
    path("webhook/<int:project_id>/<slug:slug>/", api.webhook, name="api_webhook"),
]
