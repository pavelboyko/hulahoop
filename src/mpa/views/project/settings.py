from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django import forms
from app.models import Project


class ProjectForm(forms.Form):
    pass


@login_required
def project_settings(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            # TODO update project
            return HttpResponseRedirect(
                reverse("project_settings", kwargs={"project": project})
            )
    else:
        form = ProjectForm()

    return render(
        request, "mpa/project/settings.html", {"project": project, "form": form}
    )
