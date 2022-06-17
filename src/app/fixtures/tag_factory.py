from collections import OrderedDict
from factory import Faker, SubFactory
from factory.django import DjangoModelFactory
from app.models import Tag
from .example_factory import ExampleFactory


class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag

    example = SubFactory(ExampleFactory)
    key = Faker("random_element", elements=["device.os", "make", "model"])
    value = Faker(
        "random_element",
        elements=OrderedDict(
            [
                ("red", 0.45),
                ("blue", 0.35),
                ("green", 0.15),
                ("yellow", 0.05),
            ]
        ),
    )
