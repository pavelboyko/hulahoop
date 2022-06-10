from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from app.tasks import handle_webhook


@api_view(["POST"])
def webhook(request, project_id: int, slug: str) -> Response:
    """/api/webhook/<project_id>/<slug>/ handler"""
    # TODO: validate project_id
    # TODO: add project_key to the URL
    handle_webhook.delay(project_id, slug, request.data)
    return Response(
        data={status: 1}, status=status.HTTP_200_OK
    )  # always OK because the actual webhook handler runs async
