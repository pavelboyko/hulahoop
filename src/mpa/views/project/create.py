from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django import forms
from app.models import Project


class ProjectForm(forms.Form):
    name = forms.CharField(label="Project name", max_length=100)
    description = forms.CharField(
        label="Optional description", widget=forms.Textarea(), required=False
    )


@login_required
def project_create(request):
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(
                name=form.cleaned_data["name"],
                description=form.cleaned_data["description"],
                created_by=request.user,
            )
            return HttpResponseRedirect(
                reverse("project_settings", kwargs={"project_id": project.id})
            )
    else:
        form = ProjectForm()

    return render(request, "mpa/project/create.html", {"form": form})
