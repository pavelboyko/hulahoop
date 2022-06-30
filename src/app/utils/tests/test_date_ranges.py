from django.test import TestCase
from app.utils.date_ranges import date_ranges


class Test(TestCase):
    """
    ./manage.py test app.utils.tests.test_date_ranges.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test_length(self) -> None:
        data = {
            "today": 1,
            "yesterday": 1,
            "week": 7,
            "month": 30,
            "quarter": 90,
            "year": 365,
        }

        for key, ndays in data.items():
            self.assertEqual(len(list(date_ranges[key]["dayrange"]())), ndays)
