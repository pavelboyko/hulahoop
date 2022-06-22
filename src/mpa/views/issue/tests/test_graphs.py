from imghdr import tests
from django.test import TestCase
from mpa.views.issue.graphs import plot_examples_last_n_days, plot_confusion_matrix


class Test(TestCase):
    """
    ./manage.py test mpa.views.issue.tests.test_graphs.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        pass

    def test_plot_examples_last_n_days(self) -> None:
        labels = [
            "Monday",
            "Tuesday",
            "Wednesday",
        ]
        values = [1, 2, 3]

        chart = plot_examples_last_n_days(labels, values)
        self.assertIsNotNone(chart)  # chart is created
        self.assertIsNotNone(chart.render_embed())  # at least render does not fail
