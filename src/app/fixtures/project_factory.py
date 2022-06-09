from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from django.utils.timezone import get_current_timezone
from app.fixtures.user_factory import UserFactory
from app.models import Project
from .user_factory import UserFactory


class ProjectFactory(DjangoModelFactory):
    class Meta:
        model = Project

    name = Faker("catch_phrase")
    description = Faker("paragraph", nb_sentences=1)
    properties = {
        "plugins": {
            "labeling": {
                "slug": "dummy_labeling",
                "config": {},
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
    created_by = SubFactory(UserFactory)
