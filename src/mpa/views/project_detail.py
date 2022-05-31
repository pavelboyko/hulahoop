from django.shortcuts import render, get_object_or_404
from app.models import Project, Example


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    examples = Example.objects.filter(project=project, is_deleted=False)
    context = {"project": project, "example_list": examples}
    return render(request, "mpa/project/project_detail.html", context)
