from factory import Faker, SubFactory, post_generation
from factory.django import DjangoModelFactory
from app.models import Issue
from .project_factory import ProjectFactory
from .example_factory import ExampleFactory


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    project = SubFactory(ProjectFactory)
    name = Faker("bs")

    @post_generation
    def examples(obj, create, extracted, **kwargs):
        """
        If called like: IssueFactory(examples=4) it generates an Issue with 4
        examples. If called without `examples` argument, no examples generated
        """
        if not create:
            return

        if extracted is not None:
            for _ in range(extracted):
                ExampleFactory.create(project=obj.project, issue=obj)
