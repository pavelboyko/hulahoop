from imghdr import tests
from django.test import TestCase
from mpa.views.issue.graphs import plot_example_count_daily


class Test(TestCase):
    """
    ./manage.py test mpa.views.issue.tests.test_graphs.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test_plot_example_count_daily(self) -> None:
        labels = [
            "Monday",
            "Tuesday",
            "Wednesday",
        ]
        values = [1, 2, 3]

        chart = plot_example_count_daily(labels, values)
        self.assertIsNotNone(chart)  # chart is created
        self.assertIn("svg", chart)
