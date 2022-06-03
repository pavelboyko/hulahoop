from . import label_studio


def init_plugins():
    label_studio.init(
        {
            "LABELSTUDIO_URL": "http://host.docker.internal:8080/",
            "LABELSTUDIO_API_KEY": "d3bca97b95da0820cadae2197c7ccde4ee6e77b7",
        }
    )
