from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from app.models import Project


@login_required
def project_list(request):
    projects = Project.objects.all().order_by("name")
    context = {"project_list": projects}
    return render(request, "mpa/project/list.html", context)
