from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.urls import reverse
from django import forms
from crispy_forms.helper import FormHelper
from app.models import Project, Issue


class IssueForm(forms.Form):
    name = forms.CharField(label="Issue name", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.form_show_labels = False
        self.fields["name"].widget.attrs.update({"autofocus": "autofocus", "size": 25})


@login_required
def issue_edit(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id)
    issue = get_object_or_404(Issue, id=issue_id, project=project)

    if request.method == "POST":
        form = IssueForm(request.POST)
        if form.is_valid():
            issue.name = form.cleaned_data["name"]
            issue.save(update_fields=["name"])
            return HttpResponseRedirect(
                reverse(
                    "issue_detail",
                    kwargs={"project_id": project.id, "issue_id": issue.id},  # type: ignore
                )
            )
    else:
        form = IssueForm()
        form.fields["name"].initial = issue.name

    return render(
        request,
        "mpa/issue/edit.html",
        {"project": project, "issue": issue, "form": form},
    )
