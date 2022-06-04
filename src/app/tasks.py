from uuid import UUID
from typing import Any
from hulahoop.celery import app
from app.workflow.factory import start, webhook


@app.task(name="start_workflow")
def start_workflow(project_id: UUID, example_id: UUID):
    start(project_id, example_id)


@app.task(name="handle_webhook")
def handle_webhook(project_id: UUID, slug: str, data: Any):
    webhook(project_id, slug, data)
