from typing import Optional, Any
from app.models.idof import IdOfProject, IdOfExample


class BaseWorkflow:
    project_id: IdOfProject

    def __init__(self, project_id: IdOfProject):
        self.project_id = project_id

    def start(self, example_id: IdOfExample):
        """Executed when new example is added to the project"""
        pass

    def webhook(self, slug: str, data: Any):
        """Executed when the webhook API endpoint receives data for the project"""
        pass
