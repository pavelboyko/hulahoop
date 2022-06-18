from imghdr import tests
from django.test import TestCase
from app.fixtures.example_factory import ExampleFactory
from app.models import Project
from app.fixtures import IssueFactory
from mpa.views.issue.graphs import plot_examples_last_n_days


class Test(TestCase):
    """
    ./manage.py test mpa.views.issue.tests.test_graphs.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_plot_examples_last_n_days(self) -> None:
        issue = IssueFactory.create(examples=10)
        chart = plot_examples_last_n_days(issue, ndays=100)
        self.assertIsNotNone(chart)  # at least
