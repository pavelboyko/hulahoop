import logging
import requests
from typing import Dict, Any
from urllib.parse import urljoin
from .exceptions import RestRequestError

logger = logging.getLogger(__package__)


class BaseRestClient:
    """REST helpers"""

    base_url: str = ""
    headers: Dict[str, str] = {}

    def __init__(self, base_url: str = "", headers: Dict[str, str] = {}):
        self.base_url = base_url
        self.headers = headers

    def create(self, path: str, data: Any):
        url = urljoin(self.base_url, path)
        logger.debug(f"Creating url={url}, data={data}.")
        try:
            response = requests.post(
                url=url,
                json=data,
                headers=self.headers,
            )
            if response.status_code != 201:
                RestRequestError(response.text)
        except requests.ConnectionError as e:
            raise RestRequestError(e)
