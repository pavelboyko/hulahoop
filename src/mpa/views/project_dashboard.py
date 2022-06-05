from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from app.models import Project, Example


@login_required
def project_dashboard(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    examples_last_30_days = (
        Example.objects.filter(
            project=project,
            is_deleted=False,
            created_at__gte=timezone.now() - timedelta(days=30),
        )
        .values("created_at__date", "status")
        .annotate(count=Count("id"))
        .values("created_at__date", "status", "count")
        .order_by("created_at__date")
    )

    return render(
        request,
        "mpa/project/project_dashboard.html",
        {"project": project, "examples_last_30_days": examples_last_30_days},
    )
