from django.shortcuts import render
from app.models import Project


def project_list(request):
    projects = Project.objects.filter(is_deleted=False).order_by("name")
    context = {"project_list": projects}
    return render(request, "mpa/project/project_list.html", context)
