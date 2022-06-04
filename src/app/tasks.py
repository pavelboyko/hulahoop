import uuid
from hulahoop.celery import app
from app.workflow.factory import start


@app.task(name="start_workflow")
def start_workflow(project_id: uuid.UUID, example_id: uuid.UUID):
    start(project_id, example_id)
