from django.urls import path
from mpa import views
from mpa.views import example, project, issue
from app.models.idof import (
    IdOfProjectPathConverter,
    IdOfExamplePathConverter,
    IdOfIssuePathConverter,
)

urlpatterns = [
    path("", views.index, name="index"),
    path("projects/", views.project.project_list, name="project_list"),
    path("projects/create/", views.project.project_create, name="project_create"),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/",
        views.project.project_detail,
        name="project_detail",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/examples/",
        views.example.example_list,
        name="example_list",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/settings/",
        views.project.project_settings,
        name="project_settings",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/dashboard/",
        views.project.project_dashboard,
        name="project_dashboard",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/issues/",
        views.issue.issue_list,
        name="issue_list",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/examples/<{IdOfExamplePathConverter}:example_id>/",
        views.example.example_detail,
        name="example_detail",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/issues/<{IdOfIssuePathConverter}:issue_id>",
        views.issue.issue_detail,
        name="issue_detail",
    ),
]
