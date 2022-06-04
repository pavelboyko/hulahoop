from app.models import Example


class BasePlugin:
    pass


class BaseLabelingPlugin(BasePlugin):
    def create_labeling_task(self, example: Example):
        pass
