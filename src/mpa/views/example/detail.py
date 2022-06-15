from typing import Any
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from app.models import Project, Example


@login_required
def example_detail(request, project_id, example_id):
    def pretty_print(data: Any) -> str:
        return json.dumps(data, indent=4, sort_keys=True) if data is not None else ""

    project = get_object_or_404(Project, id=project_id)
    example = get_object_or_404(Example, id=example_id, project=project)
    return render(
        request,
        "mpa/example/detail.html",
        {
            "project": project,
            "example": example,
            "predictions": pretty_print(example.predictions),
            "annotations": pretty_print(example.annotations),
            "properties": pretty_print(example.properties),
            "tags": example.exampletag_set.all(),
        },
    )
