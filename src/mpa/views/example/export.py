import json
from django.http import HttpResponse
from app.models import Example


def export_example_json(example: Example) -> HttpResponse:
    response = HttpResponse(
        json.dumps(example.to_dict()),
        content_type="application/json",
    )
    response["Content-Disposition"] = "example.json"
    return response
