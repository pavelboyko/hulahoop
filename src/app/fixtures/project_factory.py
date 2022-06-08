from factory import Faker
from factory.django import DjangoModelFactory
from django.utils.timezone import get_current_timezone
from app.models import Project


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = "Not Hotdog"
    description = "A demo project"
    properties = {
        "plugins": {
            "labeling": {
                "slug": "label_studio",
                "config": {
                    "url": "http://host.docker.internal:8080/",
                    "api_key": "d3bca97b95da0820cadae2197c7ccde4ee6e77b7",
                    "project_id": 2,
                },
            }
        }
    }
    media_type = Project.MediaType.image
    created_at = Faker(
        "date_time_between",
        start_date="-90d",
        end_date="-30d",
        tzinfo=get_current_timezone(),
    )
    created_by_id = 1
