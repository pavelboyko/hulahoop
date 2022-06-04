from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project


@login_required
def project_dashboard(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    return render(request, "mpa/project/project_dashboard.html", {"project": project})
