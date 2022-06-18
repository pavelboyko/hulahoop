from django.test import TestCase
from app.models import Project
from app.fixtures import ExampleFactory
from app.models import Tag


class Test(TestCase):
    """
    ./manage.py test app.models.tests.test_tag.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_str(self) -> None:
        example = ExampleFactory.create(tags=1)
        self.assertIn(":", str(example.tag_set.first()))
