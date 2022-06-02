from typing import Dict, Callable, Any
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

__handler_registry: Dict[str, Callable[[Any], None]] = {}


def register_webhook_handler(token: str, callback: Callable[[Any], None]) -> None:
    """Register a webhook handler
    :param token:
    :param callback:
    """
    __handler_registry[token] = callback


@api_view(["POST"])
def webhook(request, token):
    """
    Universal webhook receiver used in integrations
    """
    if token not in __handler_registry:
        return Response({"error": "Unknown token", "token": token, "data": request.data}, status.HTTP_400_BAD_REQUEST)

    __handler_registry[token](request.data)
    return Response(data={}, status=status.HTTP_200_OK)


