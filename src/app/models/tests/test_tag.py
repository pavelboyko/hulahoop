from django.test import TestCase
from app.models import Project
from app.fixtures import TagFactory


class Test(TestCase):
    """
    ./manage.py test app.models.tests.test_tag.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_str(self) -> None:
        et = TagFactory.create(key="a", value="b")
        self.assertEqual(str(et), "a:b")
