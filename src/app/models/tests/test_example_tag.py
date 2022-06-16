from django.test import TestCase
from app.models import Project
from app.fixtures import ExampleTagFactory


class Test(TestCase):
    """
    ./manage.py test app.models.tests.test_example_tag.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_str(self) -> None:
        et = ExampleTagFactory.create(key="a", value="b")
        self.assertEqual(str(et), "a:b")
