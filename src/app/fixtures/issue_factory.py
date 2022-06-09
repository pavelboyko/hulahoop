from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from app.models import Issue
from .project_factory import ProjectFactory


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    project = SubFactory(ProjectFactory)
    name = Faker("bs")
    description = Faker("paragraph", nb_sentences=2)
