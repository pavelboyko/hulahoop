from typing import Any
from hulahoop.celery import app
from app.models.idof import IdOfProject, IdOfExample
from app.workflow.factory import start, webhook


@app.task(name="start_workflow")
def start_workflow(project_id: IdOfProject, example_id: IdOfExample):
    start(project_id, example_id)


@app.task(name="handle_webhook")
def handle_webhook(project_id: IdOfProject, slug: str, data: Any):
    webhook(project_id, slug, data)
