from typing import Dict, Callable, Any
import logging
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from app.tasks import handle_webhook

logger = logging.getLogger(__package__)


@api_view(["POST"])
def webhook(request, project_id, slug):
    """/api/v1.0/webhook/<project_id>/<slug>/ handler"""
    handle_webhook.delay(project_id, slug, request.data)
    return Response(
        data={}, status=status.HTTP_200_OK
    )  # always OK because the actual webhook handler runs async
