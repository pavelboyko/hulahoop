from django.urls import path
from mpa.views import index, project, example, issue

urlpatterns = [
    path("", index, name="index"),
    path("projects/", project.project_list, name="project_list"),
    path("projects/create/", project.project_create, name="project_create"),
    path("projects/<int:project_id>/", project.project_detail, name="project_detail"),
    path(
        "projects/<int:project_id>/settings/",
        project.project_settings,
        name="project_settings",
    ),
    path("projects/<int:project_id>/issues/", issue.issue_list, name="issue_list"),
    path(
        "projects/<int:project_id>/examples/<uuid:example_id>/",
        example.example_detail,
        name="example_detail",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>",
        issue.issue_detail,
        name="issue_detail",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/edit/",
        issue.issue_edit,
        name="issue_edit",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/change_status/",
        issue.issue_change_status,
        name="issue_change_status",
    ),
    path(
        "projects/<int:project_id>/issues/<int:issue_id>/activity/",
        issue.issue_activity,
        name="issue_activity",
    ),
]
