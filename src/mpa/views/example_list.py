from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
import django_filters
from app.models import Project, Example


class ExampleFilter(django_filters.FilterSet):
    created_at = django_filters.DateRangeFilter()

    class Meta:
        model = Example
        fields = ["status", "created_at"]


@login_required
def example_list(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    example_filter = ExampleFilter(
        request.GET, queryset=Example.objects.filter(project=project, is_deleted=False)
    )

    context = {"project": project, "example_filter": example_filter}
    return render(request, "mpa/example/example_list.html", context)
