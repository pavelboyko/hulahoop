from django.test import TestCase
from app.utils.fix_docker_hostname import fix_docker_hostname


class Test(TestCase):
    """
    ./manage.py test app.utils.tests.test_fix_docker_hostname.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test(self) -> None:
        self.assertEqual(fix_docker_hostname("localhost"), "host.docker.internal")
