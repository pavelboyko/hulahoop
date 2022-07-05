import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project, Issue

logger = logging.getLogger(__package__)


@login_required
def issue_activity(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id)
    issue = get_object_or_404(Issue, id=issue_id, project=project)

    return render(
        request,
        "mpa/issue/activity.html",
        {
            "project": project,
            "issue": issue,
        },
    )