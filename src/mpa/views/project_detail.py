from django.shortcuts import render, get_object_or_404
import django_filters
from app.models import Project, Example


class ExampleFilter(django_filters.FilterSet):
    created_at = django_filters.DateRangeFilter()

    class Meta:
        model = Example
        fields = ['created_at', 'status']


def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    example_filter = ExampleFilter(request.GET, queryset=Example.objects.filter(project=project, is_deleted=False))

    context = {"project": project, "example_filter": example_filter}
    return render(request, "mpa/project/project_detail.html", context)
