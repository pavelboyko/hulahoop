from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project, Issue


@login_required
def issue_detail(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    issue = get_object_or_404(
        Issue, id=issue_id, project=project, is_deleted=False
    )
    context = {"project": project, "issue": issue}
    return render(request, "mpa/issue/detail.html", context)
