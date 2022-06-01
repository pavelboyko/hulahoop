"""
This is a demo workflow, to be better understood and generalized later on
"""
import logging
from app.models.example import Example

logger = logging.getLogger(__package__)


def start(example: Example) -> None:
    logger.debug(f"Started demo workflow for example {example}")
    create_labeling_task(example)


def create_labeling_task(example: Example) -> None:
    logger.debug(f"Creating labeling task for example {example}")
