from typing import Dict, Any
from app.plugins.base import BasePlugin
from .client import LabelStudioClient


class LabelStudioPlugin(BasePlugin):
    name: str = "Label Studio"
    slug: str = "labelstudio"
    client: LabelStudioClient = None

    def __init__(self, config: Dict[str, Any]):
        self.client = LabelStudioClient(config)
