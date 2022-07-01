from django.test import TestCase
from app.utils.json_stream import json_stream


class Test(TestCase):
    """
    ./manage.py test app.utils.tests.test_json_stream.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test(self) -> None:
        data = [1, 2, 3]
        out = list(json_stream(data, len(data)))
        self.assertListEqual(out, ["[", "1,", "2,", "3", "]"])

    def test_empty(self) -> None:
        data = []
        out = list(json_stream(data, len(data)))
        self.assertListEqual(out, ["[", "]"])
