from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Count
from app.models import Project
from .project_filter import ProjectFilter


@login_required
def project_list(request):
    projects = Project.objects.all().annotate(issues=Count("issue"))
    filter = ProjectFilter(request.GET, queryset=projects)
    return render(request, "mpa/project/list.html", {"filter": filter})
