import logging
from typing import Dict, Optional, Type, Any
from app.models.idof import IdOfProject
from .base import BaseLabelingPlugin
from .label_studio import LabelStudioPlugin
from .dummy import DummyLabelingPlugin

logger = logging.getLogger(__package__)

# We will make the registry more dynamic in the future to allow 3rd party plugins
labeling_plugins: Dict[str, Type[BaseLabelingPlugin]] = {
    LabelStudioPlugin.slug: LabelStudioPlugin,
    DummyLabelingPlugin.slug: DummyLabelingPlugin,
}


def build_labeling_plugin(
    project_id: IdOfProject, slug: str, config: Any
) -> Optional[BaseLabelingPlugin]:
    if slug in labeling_plugins:
        return labeling_plugins[slug](project_id, config)

    logger.error(f"Unknown labeling plugin slug: {slug} project_id={project_id}")
