import logging
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django import forms
from app.models import Project, Issue

logger = logging.getLogger(__package__)


@login_required
@require_POST
def issue_change_status(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id)
    issue = get_object_or_404(Issue, id=issue_id, project=project)

    logger.info(request.POST)

    if "action" in request.POST:
        match request.POST["action"]:
            case "reopen":
                issue.reopen()
            case "mute":
                issue.mute()
            case "resolve":
                issue.resolve()
            case "close":
                issue.close()

    return HttpResponseRedirect(
        reverse(
            "issue_detail",
            kwargs={"project_id": project.id, "issue_id": issue.id},  # type: ignore
        )
    )
