from django.shortcuts import render
from app.models import Project


def index(request):
    projects = Project.objects.filter(is_deleted=False)
    context = {"project_list": projects}
    return render(request, "mpa/index/index.html", context)
