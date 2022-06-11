from django.urls import path
from mpa.views import index, project, example, issue
from app.models.idof import (
    IdOfProjectPathConverter,
    IdOfExamplePathConverter,
    IdOfIssuePathConverter,
)

urlpatterns = [
    path("", index, name="index"),
    path("projects/", project.project_list, name="project_list"),
    path("projects/create/", project.project_create, name="project_create"),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/",
        project.project_detail,
        name="project_detail",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/examples/",
        example.example_list,
        name="example_list",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/settings/",
        project.project_settings,
        name="project_settings",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/issues/",
        issue.issue_list,
        name="issue_list",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/examples/<{IdOfExamplePathConverter}:example_id>/",
        example.example_detail,
        name="example_detail",
    ),
    path(
        f"projects/<{IdOfProjectPathConverter}:project_id>/issues/<{IdOfIssuePathConverter}:issue_id>",
        issue.issue_detail,
        name="issue_detail",
    ),
]
