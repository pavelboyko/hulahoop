import logging
import requests
from typing import Dict, Any
from urllib.parse import urljoin

logger = logging.getLogger(__package__)


class RestClient:
    class RequestError(Exception):
        pass

    base_url: str = ""
    headers: Dict[str, str] = {}

    def __init__(self, base_url: str = "", headers: Dict[str, str] = {}):
        self.base_url = base_url
        self.headers = headers

    def get(self, path: str) -> Any:
        url = urljoin(self.base_url, path)
        logger.debug(f"GET url={url}.")
        try:
            response = requests.get(url=url, headers=self.headers)
            if response.status_code != 200:
                raise RestClient.RequestError(response.text)
            return response.json()
        except requests.ConnectionError as e:
            raise RestClient.RequestError(e)

    def create(self, path: str, data: Any) -> None:
        url = urljoin(self.base_url, path)
        logger.debug(f"POST url={url}, data={data}.")
        try:
            response = requests.post(
                url=url,
                json=data,
                headers=self.headers,
            )
            if response.status_code != 201:
                raise RestClient.RequestError(response.text)
        except requests.ConnectionError as e:
            raise RestClient.RequestError(e)
