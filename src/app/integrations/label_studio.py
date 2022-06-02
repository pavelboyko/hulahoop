from typing import Tuple, Any
import logging
import requests
from urllib.parse import urljoin
from app.api import register_webhook_handler

logger = logging.getLogger(__package__)


def create_image_labeling_task(
    label_studio_url: str,
    label_studio_api_key: str,
    label_studio_project_id: str,
    image_url: str,
) -> Tuple[bool, str]:
    """Create a single image labeling task in Label Studio

    :param label_studio_url:        Root Label Studio URL, e.g. "https://mydomain.com/".
                                    For local deployments with Docker use a special domain host.docker.internal
                                    to access Label Studio from within Hulahoop container,
                                    e.g. label_studio_url="http://host.docker.internal:8080/"
    :param label_studio_api_key:    A secret Label Studio API key.
                                    You can find your API key on the User Account page in Label Studio.
    :param label_studio_project_id: A Label Stuio project ID. Up to my knowledge it can only be found in the URL, e.g.
                                    if the URL is "http://localhost:8080/projects/2/data?tab=2" than the project ID is
                                    2. Label Studio uses integer project IDs but we here receive it as string just
                                    in case they will change their minds and use more secure IDs.
    :param image_url:               An absolute URL of the image to be labeled. The URL must be accessible without
                                    authorization.

    :return: the tuple (success, error message || empty string)
    """
    request_url = urljoin(
        label_studio_url, f"api/projects/{label_studio_project_id}/import"
    )
    request_data = [{"image": image_url}]
    logger.debug(
        f"Creating Label Studio task: request_url={request_url}, request_data={request_data}"
    )
    try:
        response = requests.post(
            url=request_url,
            json=request_data,
            headers={"Authorization": f"Token {label_studio_api_key}"},
        )
        if response.status_code != 201:
            logger.error(f"Failed to create Label Studio task: {response.text}")
            return False, response.text
        else:
            logger.debug(f"Label Studio task successfully created: {response.text}")
            return True, ""
    except requests.ConnectionError as e:
        logger.error(f"Failed to connect to Label Studio: {e}")
        return False, e.strerror


def webhook_handler(data: Any) -> None:
    logger.info(f"Label Studio webhook received some data: {data}")


register_webhook_handler("labelstudio", webhook_handler)