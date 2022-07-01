from django.http import StreamingHttpResponse
from django.db.models import QuerySet
from app.models import Example
from app.utils.json_stream import json_stream


def export_json(examples: QuerySet[Example], count: int) -> StreamingHttpResponse:
    response = StreamingHttpResponse(
        json_stream((example.to_dict() for example in examples), count),
        content_type="application/json",
    )
    response["Content-Disposition"] = "examples.json"
    return response
