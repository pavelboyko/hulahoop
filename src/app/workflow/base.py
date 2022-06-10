from typing import Any, List
from app.plugins import BasePlugin
from app.models.idof import IdOfProject, IdOfExample


class BaseWorkflow:
    project_id: IdOfProject
    webhook_receivers: List[BasePlugin] = []

    def __init__(self, project_id: IdOfProject):
        self.project_id = project_id

    def start(self, example_id: IdOfExample) -> None:
        """Executed when new example is added to the project"""
        pass

    def webhook(self, slug: str, data: Any) -> None:
        """Executed when the webhook API endpoint receives data for the project"""
        for p in self.webhook_receivers:
            if p.slug == slug:
                p.receive_webhook(data)
