from factory.django import DjangoModelFactory
from app.models import Project, Issue


class IssueFactory(DjangoModelFactory):
    class Meta:
        model = Issue

    def __init__(self, project: Project):
        self.project = project

    name = "Cartoonish hotdogs"
    description = "Cartoon style images of hot dogs are not properly classified"
