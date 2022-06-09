import django
from django.test import TestCase
from app.models import Project
from app.fixtures import UserFactory


class Test(TestCase):
    """
    ./manage.py test app.fixtures.tests.test_user_factory.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test(self) -> None:
        user = UserFactory()
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.email)
