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

    def get(self, path: str) -> Any:
        url = urljoin(self.base_url, path)
        logger.debug(f"Get url={url}.")
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code != 200:
                raise RestRequestError(response.text)
            return response.json()
        except requests.ConnectionError as e:
            raise RestRequestError(e)

    def create(self, path: str, data: Any) -> None:
        url = urljoin(self.base_url, path)
        logger.debug(f"Creating url={url}, data={data}.")
        try:
            response = requests.post(
                url=url,
                json=data,
                headers=self.headers,
            )
            if response.status_code != 201:
                raise RestRequestError(response.text)
        except requests.ConnectionError as e:
            raise RestRequestError(e)
