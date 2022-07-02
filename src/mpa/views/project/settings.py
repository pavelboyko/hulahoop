from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from app.models import Project
from hulahoop.settings import HTTP_SCHEME, HOSTNAME


class RenameForm(forms.Form):
    name = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.helper.add_input(Submit("submit_rename", "Rename"))


class ArchiveForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(
            Submit("submit_archive", "Archive", css_class="btn-danger")
        )


@login_required
def project_settings(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    capture_endpoint = (
        f"{HTTP_SCHEME}://{HOSTNAME}{reverse('api_capture', args=[project_id])}"
    )
    rename_form = RenameForm()
    rename_form.fields["name"].initial = project.name
    archive_form = ArchiveForm()

    if request.method == "POST":
        if "submit_rename" in request.POST:
            rename_form = RenameForm(request.POST)
            if rename_form.is_valid():
                project.name = rename_form.cleaned_data["name"]
                project.save(update_fields=["name"])

    return render(
        request,
        "mpa/project/settings.html",
        {
            "project": project,
            "capture_endpoint": capture_endpoint,
            "rename_form": rename_form,
            "archive_form": archive_form,
        },
    )
