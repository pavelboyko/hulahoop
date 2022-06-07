from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project, Example


@login_required
def example_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    examples = Example.objects.filter(project=project).order_by("-id")
    return render(
        request,
        "mpa/example/list.html",
        {"project": project, "examples": examples},
    )
