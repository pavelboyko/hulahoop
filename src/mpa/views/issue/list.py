from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from app.models import Project, Issue
from .issue_filter import IssueFilter


@login_required
def issue_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    issues = project.issue_set.annotate(examples=Count("example"))  # type: ignore
    filter = IssueFilter(request.GET, queryset=issues)
    return render(
        request,
        "mpa/issue/list.html",
        {"project": project, "issues": issues, "filter": filter},
    )
