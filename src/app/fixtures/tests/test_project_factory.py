from django.test import TestCase
from app.fixtures import ProjectFactory


class Test(TestCase):
    """
    ./manage.py test app.fixtures.tests.test_project_factory.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test(self) -> None:
        p = ProjectFactory()
        self.assertIsNotNone(p.name)
        self.assertIsNotNone(p.description)
        self.assertIsNotNone(p.properties)
        self.assertIsNotNone(p.created_at)
        self.assertIsNotNone(p.created_by)
