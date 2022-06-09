from factory import Faker
from factory.django import DjangoModelFactory
from app.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = Faker("name")
    email = Faker("email")
