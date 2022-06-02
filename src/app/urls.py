from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from app import api

# Api v1.0
api_router = routers.DefaultRouter()
api_router.register(r"projects", api.ProjectViewSet, basename="projects_v1_0")
api_router.register(r"examples", api.ExampleViewSet, basename="examples_v1_0")

urlpatterns = [
    path(r"v1.0/", include(api_router.urls)),
    path(r"v1.0/webhook/<token>/", api.webhook, name="webhook_v1_0"),
]
