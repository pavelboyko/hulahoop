from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import django_filters
from crispy_forms.helper import FormHelper
from django.db.models import Count
from app.models import Project, Issue


class IssueFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains", label="Search issues by name"
    )
    examples__gt = django_filters.NumberFilter(
        field_name="examples", lookup_expr="gt", label="Min examples"
    )
    order = django_filters.OrderingFilter(
        choices=(
            ("-examples", "Examples"),
            ("-updated_at", "Last seen"),
            ("-created_at", "First seen"),
        ),
    )

    class Meta:
        model = Issue
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
        self.form.helper.label_class = "text-muted"


@login_required
def issue_list(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    issues = project.issue_set.annotate(examples=Count("example"))
    filter = IssueFilter(request.GET, queryset=issues)
    return render(
        request,
        "mpa/issue/list.html",
        {"project": project, "filter": None, "issues": issues, "filter": filter},
    )
