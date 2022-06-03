from typing import Dict, Callable, Any
import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from urllib.parse import urljoin, quote
from hulahoop.settings import HOSTNAME, HTTP_SCHEME, API_VERSION

logger = logging.getLogger(__package__)

__handler_registry: Dict[str, Callable[[Any], None]] = {}


def register_webhook_handler(slug: str, callback: Callable[[Any], None]) -> None:
    """Register a webhook handler which will be called on POST to /api/v1.0/webhook/<slug>/
    :param slug:        Unique webhook slug
    :param callback:    Callable which is called on POST to /api/v1.0/webhook/<slug>/
    """
    global __handler_registry

    __handler_registry[slug] = callback
    logger.info(f"Webhook slug '{slug}' registered")


def get_webhook_absolute_url(slug: str) -> str:
    """Get a registered webhook URL for a slug"""
    return urljoin(
        f"{HTTP_SCHEME}{HOSTNAME}", f"api/v{API_VERSION}/webhook/{quote(slug)}/"
    )


@api_view(["POST"])
def webhook(request, slug):
    """/api/v1.0/webhook/<slug>/ handler"""
    if slug not in __handler_registry:
        return Response(data={}, status=status.HTTP_404_NOT_FOUND)

    callback = __handler_registry[slug]
    callback(request.data)
    return Response(data={}, status=status.HTTP_200_OK)
