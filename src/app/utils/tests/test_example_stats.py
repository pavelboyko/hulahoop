from __future__ import annotations
from optparse import Values
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from app.models import Example, Project, Tag
from app.fixtures import ExampleFactory, IssueFactory
from app.utils.example_stats import (
    issue_example_count,
    issue_example_count_last_n_days,
    issue_tag_values_count,
    examples_confusion_matrix,
    ColoredCounter,
)


class Test(TestCase):
    """
    ./manage.py test app.utils.tests.test_example_stats.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_issue_example_count(self) -> None:
        issue = IssueFactory.create()
        ExampleFactory.create(project=issue.project, issue=issue)
        self.assertEqual(issue_example_count(issue), 1)

    def test_issue_example_count_last_n_days(self) -> None:
        issue = IssueFactory.create()
        for days in range(10):
            ExampleFactory.create(
                project=issue.project,
                issue=issue,
                created_at=timezone.now() - timedelta(days=days),
            )
        labels, values = issue_example_count_last_n_days(issue, ndays=5)
        self.assertEqual(len(labels), 5)
        self.assertListEqual(values, [1] * 5)

    def test_issue_tag_values_count(self) -> None:
        issue = IssueFactory.create()
        example1 = ExampleFactory.create(project=issue.project, issue=issue, tags=0)
        Tag.objects.create(example=example1, key="key_1", value="value_1")
        Tag.objects.create(example=example1, key="key_2", value="value_21")
        example2 = ExampleFactory.create(project=issue.project, issue=issue, tags=0)
        Tag.objects.create(example=example2, key="key_1", value="value_1")
        Tag.objects.create(example=example2, key="key_2", value="value_22")
        tag_count = issue_tag_values_count(issue)
        self.assertTrue("key_1" in tag_count)
        self.assertTrue("key_2" in tag_count)
        self.assertEqual(len(tag_count["key_1"]), 1)
        self.assertEqual(tag_count["key_1"][0], ColoredCounter("value_1", 2, 100.0))
        self.assertEqual(len(tag_count["key_2"]), 2)
        self.assertSetEqual(
            set(tag_count["key_2"]),
            set(
                [
                    ColoredCounter("value_21", 1, 50.0),
                    ColoredCounter("value_22", 1, 50.0),
                ]
            ),
        )

    def test_examples_confusion_matrix_empty(self) -> None:
        ExampleFactory.create(predictions={}, annotations={})
        labels, values = examples_confusion_matrix(Example.objects.all())
        print(values)
        self.assertListEqual(labels, ["None"])
        self.assertListEqual(values, [(0, 0, 1)])

    def test_examples_confusion_matrix_2x2_full(self) -> None:
        for p in ["a", "b"]:
            for a in ["a", "b"]:
                ExampleFactory.create(
                    predictions={"label": p}, annotations={"label": a}
                )
        labels, values = examples_confusion_matrix(Example.objects.all())
        self.assertListEqual(labels, ["a", "b"])
        self.assertListEqual(values, [(0, 0, 1), (0, 1, 1), (1, 0, 1), (1, 1, 1)])

    def test_examples_confusion_matrix_2x2(self) -> None:
        ExampleFactory.create(predictions={"label": "b"}, annotations={"label": "a"})
        labels, values = examples_confusion_matrix(Example.objects.all())
        self.assertListEqual(labels, ["a", "b"])
        self.assertListEqual(values, [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 0)])

    def test_examples_confusion_matrix_1x2(self) -> None:
        ExampleFactory.create(predictions={"label": "a"}, annotations=None)
        labels, values = examples_confusion_matrix(Example.objects.all())
        self.assertListEqual(labels, ["None", "a"])
        self.assertListEqual(values, [(0, 0, 0), (0, 1, 1), (1, 0, 0), (1, 1, 0)])
