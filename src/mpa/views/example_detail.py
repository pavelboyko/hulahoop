from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project, Example, ExampleEvent


@login_required
def example_detail(request, project_id, example_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    example = get_object_or_404(
        Example, id=example_id, project=project, is_deleted=False
    )
    event_list = ExampleEvent.objects.filter(example_id=example_id).order_by("created_at")
    context = {"project": project, "example": example, "event_list": event_list}
    return render(request, "mpa/example/example_detail.html", context)
