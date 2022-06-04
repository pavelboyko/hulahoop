from django.urls import path
from mpa import views

urlpatterns = [
    path("", views.index, name="index"),
    path("projects/", views.project_list, name="project_list"),
    path("projects/create/", views.project_create, name="project_create"),
    path("projects/<uuid:project_id>/", views.project_detail, name="project_detail"),
    path(
        "projects/<uuid:project_id>/examples/", views.example_list, name="example_list"
    ),
    path(
        "projects/<uuid:project_id>/settings/",
        views.project_settings,
        name="project_settings",
    ),
    path(
        "projects/<uuid:project_id>/dashboard/",
        views.project_dashboard,
        name="project_dashboard",
    ),
    path(
        "projects/<uuid:project_id>/issues/",
        views.project_issues,
        name="project_issues",
    ),
    path(
        "projects/<uuid:project_id>/examples/<uuid:example_id>/",
        views.example_detail,
        name="example_detail",
    ),
]
