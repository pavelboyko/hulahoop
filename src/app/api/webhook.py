from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from app.models import Project
from app.tasks import handle_webhook


@api_view(["POST"])
def webhook(request, project_id: int, slug: str) -> Response:
    """/api/webhook/<project_id>/<slug>/ handler"""
    get_object_or_404(Project, pk=project_id)
    handle_webhook.delay(project_id, slug, request.data)
    return Response(
        data={"status": 1}, status=status.HTTP_200_OK
    )  # always OK because the actual webhook handler runs async
