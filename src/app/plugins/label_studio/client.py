import logging
from typing import Dict, Any, Optional, Callable
from app.plugins.base import BaseRestClient, ConfigError

logger = logging.getLogger(__package__)


class LabelStudioClient(BaseRestClient):
    """REST client for Label Studio API, see https://labelstud.io/api"""

    url: Optional[str] = None
    api_key: Optional[str] = None
    project_id: Optional[int] = None

    def __init__(self, config: Dict[str, Any]):
        logger.debug(f"Initializing LabelStudioClient config={config}")
        self.read_config(config)
        super().__init__(
            base_url=self.url, headers={"Authorization": f"Token {self.api_key}"}
        )

    def read_config(self, config: Dict[str, Any]) -> None:
        self.url = config.get("LABELSTUDIO_URL")
        if not self.url:
            raise ConfigError("Missing required LABELSTUDIO_URL field")
        # TODO: check URL format

        self.api_key = config.get("LABELSTUDIO_API_KEY")
        if not self.api_key:
            raise ConfigError("Missing required LABELSTUDIO_API_KEY field")
        # TODO: check API key length

        self.project_id = config.get("LABELSTUDIO_PROJECT_ID")
        if not self.project_id:
            raise ConfigError("Missing required LABELSTUDIO_PROJECT_ID field")
        # TODO: check project id is positive integer

    def create_image_labeling_task(self, image_url: str) -> None:
        """Create an image labeling task in Label Studio.
        Request format is based on https://github.com/heartexlabs/label-studio/blob/develop/label_studio/data_import/api.py
        """
        self.create(
            path=f"/api/projects/{self.project_id}/import/",
            data=[{"image": image_url}],
        )

    def create_webhook(self, url: str) -> None:
        """Register webhook in Label Studio"""
        self.create(
            path=f"/api/webhooks/",
            data={
                "project": self.project_id,
                "url": url,
                "send_payload": True,
                "send_for_all_actions": False,
                "actions": [
                    "ANNOTATION_CREATED",
                    "ANNOTATIONS_CREATED",
                    "ANNOTATION_UPDATED",
                    "ANNOTATIONS_DELETED",
                    "TASKS_DELETED",
                ],
            },
        )
