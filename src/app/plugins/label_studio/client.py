import logging
from typing import Dict, Any, Optional
from app.models.idof import IdOfExample
from app.plugins.base import (
    BaseRestClient,
    BaseLabelingPlugin,
    ConfigError,
    RestRequestError,
)

logger = logging.getLogger(__package__)


class LabelStudioClient(BaseRestClient):
    """REST client for Label Studio API, see https://labelstud.io/api"""

    url: Optional[str] = None
    api_key: Optional[str] = None
    project_id: Optional[int] = None
    token_field: str = "hulahoop_token"

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

        self.api_key = config.get("LABELSTUDIO_API_KEY")
        if not self.api_key:
            raise ConfigError("Missing required LABELSTUDIO_API_KEY field")

        self.project_id = config.get("LABELSTUDIO_PROJECT_ID")
        if not self.project_id:
            raise ConfigError("Missing required LABELSTUDIO_PROJECT_ID field")

    def create_image_labeling_task(
        self, example_id: IdOfExample, image_url: str
    ) -> None:
        """Create an image labeling task in Label Studio.
        Request format is based on https://github.com/heartexlabs/label-studio/blob/develop/label_studio/data_import/api.py
        """
        self.create(
            path=f"/api/projects/{self.project_id}/import",  # NB! no slash at the end
            data={"image": image_url, self.token_field: str(example_id)},
        )

    def check_webhook_exists(self, url: str) -> bool:
        """Check if a given webhook url already registered in Label Studio"""
        try:
            webhooks = self.get(path=f"/api/webhooks/")
            for wh in webhooks:
                if wh["url"] == url:
                    return True
            return False
        except (TypeError, ValueError, KeyError) as e:
            raise RestRequestError(e)

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

    def get_example_id_from_webhook_request(self, data: Any) -> Optional[IdOfExample]:
        try:
            return IdOfExample(data["task"]["data"][self.token_field])
        except (ValueError, KeyError, TypeError):
            return None

    def get_action_from_webhook_request(self, data: Any) -> BaseLabelingPlugin.Action:
        try:
            action_map = {
                "ANNOTATION_CREATED": BaseLabelingPlugin.Action.ANNOTATION_CREATED,
                "ANNOTATIONS_CREATED": BaseLabelingPlugin.Action.ANNOTATION_CREATED,
                "ANNOTATION_UPDATED": BaseLabelingPlugin.Action.ANNOTATION_UPDATED,
                "ANNOTATIONS_UPDATED": BaseLabelingPlugin.Action.ANNOTATION_CREATED,
                "ANNOTATIONS_DELETED": BaseLabelingPlugin.Action.ANNOTATION_DELETED,
            }
            return action_map[data["action"]]
        except (KeyError, TypeError):
            return None

    def get_result_from_webhook_request(self, data: Any) -> Any:
        try:
            return data["annotation"]["result"]
        except (KeyError, TypeError):
            return None
