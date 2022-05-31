from django.urls import path
from mpa import views

urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("projects/<uuid:project_id>/", views.project_detail, name="project_detail"),
    path("projects/create/", views.project_create, name="project_create"),
    path(
        "projects/<uuid:project_id>/examples/<uuid:example_id>/",
        views.example_detail,
        name="example_detail",
    ),
]