from django.test import TestCase
from app.models import Project
from app.fixtures import ProjectFactory


class Test(TestCase):
    """
    ./manage.py test app.fixtures.tests.test_project_factory.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test(self) -> None:
        p = ProjectFactory()
        self.assertIsNotNone(p.name)
        self.assertIsNotNone(p.properties)
        self.assertIsNotNone(p.created_at)
        self.assertIsNotNone(p.created_by)
