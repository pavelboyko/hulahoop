from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django import forms
from app.models import Project


class ProjectForm(forms.Form):
    name = forms.CharField(label="Project name", max_length=100)


def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(
                name=form.cleaned_data["name"], created_by=request.user
            )
            return HttpResponseRedirect(
                reverse("project_detail", kwargs={"project_id": project.id})
            )
    else:
        form = ProjectForm()

    return render(request, "mpa/project/project_create.html", {"form": form})
