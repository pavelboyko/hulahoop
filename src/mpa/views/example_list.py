from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project, Example


@login_required
def example_list(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    examples = Example.objects.filter(is_deleted=False, project=project).order_by(
        "-created_at"
    )
    return render(
        request,
        "mpa/example/example_list.html",
        {"project": project, "examples": examples},
    )
