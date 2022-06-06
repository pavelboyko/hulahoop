from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.models import Project


@login_required
def project_list(request):
    projects = Project.objects.filter(is_deleted=False).order_by("name")
    context = {"project_list": projects}
    return render(request, "mpa/project/list.html", context)
