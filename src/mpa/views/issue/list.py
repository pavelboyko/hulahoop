from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project


@login_required
def issue_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    issues = project.issue_set.order_by("-updated_at")
    return render(
        request, "mpa/issue/list.html", {"project": project, "issues": issues}
    )