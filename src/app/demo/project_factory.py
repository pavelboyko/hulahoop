from factory import Faker
from factory.django import DjangoModelFactory
from django.utils.timezone import get_current_timezone
from app.models import Project


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = "Not Hotdog"
    media_type = Project.MediaType.image
    created_at = Faker(
        "date_time_between",
        start_date="-90d",
        end_date="-30d",
        tzinfo=get_current_timezone(),
    )
    created_by_id = 1
