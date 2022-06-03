"""Label Stuio integration https://labelstud.io/
Settings:
    LABELSTUDIO_URL:       Root Label Studio URL, e.g. "https://mydomain.com/".
                           For local deployments with Docker use a special domain host.docker.internal
                           to access Label Studio from within Hulahoop container,
                           e.g. label_studio_url="http://host.docker.internal:8080/"
    LABELSTUDIO_API_KEY:   A secret Label Studio API key.
                           You can find your API key on the User Account page in Label Studio.
"""
from typing import Tuple, Any, Dict
import logging
import requests
from urllib.parse import urljoin
from app.api.webhook import register_webhook_handler, get_webhook_absolute_url

logger = logging.getLogger(__package__)

plugin_name: str = "Label Studio"
slug: str = "labelstudio"
param_url: str = "LABELSTUDIO_URL"
param_api_key: str = "LABELSTUDIO_API_KEY"
config: Dict[str, str] = {}
initialized: bool = False


def init(params: Dict[str, str]) -> bool:
    global config, initialized

    logger.debug(f"Initializing {plugin_name} plugin...")
    for param in (param_url, param_api_key):
        if not param in params:
            logger.error(f"Missing '{param}' parameter, aborted.")
            return False
    config = params

    register_webhook_handler(slug, webhook_handler)
    success, message = create_webhook()
    if not success:
        return False

    initialized = True
    return True


def create_webhook() -> Tuple[bool, str]:
    """Register our webhook in Label Studio to receive updates"""
    return create_object(
        url=urljoin(config[param_url], f"api/webhooks/"),
        data={
            "url": get_webhook_absolute_url(slug),
            "send_payload": True,
            "send_for_all_actions": True,
            "headers": {},  # Authorization header here
        },
        object_name="webhook",
    )


def create_image_labeling_task(
    label_studio_project_id: int,
    image_url: str,
) -> Tuple[bool, str]:
    """Create a single image labeling task in Label Studio

    :param label_studio_project_id: A Label Stuio project ID. Up to my knowledge it can only be found in the URL, e.g.
                                    if the URL is "http://localhost:8080/projects/2/data?tab=2" than the project ID is
                                    2.
    :param image_url:               An absolute URL of the image to be labeled. The URL must be accessible without
                                    authorization.

    :return: the tuple (success, error message || empty string)
    """
    if not initialized:
        return False, "Plugin not initialized"

    return create_object(
        url=urljoin(
            config[param_url], f"api/projects/{label_studio_project_id}/import"
        ),
        data=[{"image": image_url}],
        object_name="task",
    )


def webhook_handler(data: Any) -> None:
    if not initialized:
        return
    logger.info(f"Label Studio webhook received some data: {data}")


def create_object(url: str, data: Any, object_name: str) -> Tuple[bool, str]:
    """ """
    logger.debug(f"Creating {plugin_name} {object_name}: url={url}, data={data}")
    try:
        response = requests.post(
            url=url,
            json=data,
            headers={"Authorization": f"Token {config[param_api_key]}"},
        )
        if response.status_code != 201:
            logger.error(
                f"Failed to create {plugin_name} {object_name}: {response.text}"
            )
            return False, response.text
        else:
            logger.debug(
                f"{plugin_name} {object_name} successfully created: {response.text}"
            )
            return True, ""
    except requests.ConnectionError as e:
        logger.error(f"Failed to connect to {plugin_name}: {e}")
        return False, e.strerror
