from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from app.models import Project
from hulahoop.settings import HTTP_SCHEME, HOSTNAME


@login_required
def project_settings(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    capture_endpoint = (
        f"{HTTP_SCHEME}{HOSTNAME}{reverse('api_capture', args=[project_id])}"
    )
    return render(
        request,
        "mpa/project/settings.html",
        {"project": project, "capture_endpoint": capture_endpoint},
    )
