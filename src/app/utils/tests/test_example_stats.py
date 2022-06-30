from datetime import timedelta
from django.test import TestCase
from django.utils.timezone import now
from datetime import timedelta
from app.models import Example, Project, Tag
from app.fixtures import ExampleFactory, IssueFactory
from app.utils.example_stats import (
    example_count,
    example_count_daily,
    tag_values_count,
    confusion_matrix,
    primary_color,
    ColoredCounter,
    ColoredMatrixValue,
)


class Test(TestCase):
    """
    ./manage.py test app.utils.tests.test_example_stats.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_example_count(self) -> None:
        issue = IssueFactory.create(examples=4)
        self.assertEqual(example_count(issue), 4)

    def test_example_count_daily(self) -> None:
        issue = IssueFactory.create()
        for days in range(10):
            for _ in range(2):
                ExampleFactory.create(
                    project=issue.project,
                    issue=issue,
                    created_at=now() - timedelta(days=days),
                )
        labels, values = example_count_daily(
            issue.example_set.all(),
            ((now() - timedelta(days=5 - x)).date() for x in range(5)),
        )
        self.assertEqual(len(labels), 5)
        self.assertListEqual(values, [2] * 5)

    def test_tag_values_count(self) -> None:
        secondary_color = "#1461a8"

        issue = IssueFactory.create()
        example1 = ExampleFactory.create(project=issue.project, issue=issue, tags=0)
        Tag.objects.create(example=example1, key="key_1", value="value_1")
        Tag.objects.create(example=example1, key="key_2", value="value_21")
        example2 = ExampleFactory.create(project=issue.project, issue=issue, tags=0)
        Tag.objects.create(example=example2, key="key_1", value="value_1")
        Tag.objects.create(example=example2, key="key_2", value="value_22")
        tag_count = tag_values_count(issue.example_set.all())
        self.assertTrue("key_1" in tag_count)
        self.assertTrue("key_2" in tag_count)
        self.assertEqual(len(tag_count["key_1"]), 1)
        self.assertEqual(
            tag_count["key_1"][0], ColoredCounter("value_1", 2, 100.0, primary_color)
        )
        self.assertEqual(len(tag_count["key_2"]), 2)
        ans = [
            ColoredCounter("value_21", 1, 50.0, primary_color),
            ColoredCounter("value_22", 1, 50.0, secondary_color),
        ]
        res = tag_count["key_2"]
        self.assertTrue(
            (res[0] == ans[0] and res[1] == ans[1])
            or (res[0] == ans[1] and res[1] == ans[0])
        )

    def test_confusion_matrix_empty(self) -> None:
        matrix = confusion_matrix(Example.objects.all())
        self.assertListEqual(matrix, [])

    def test_confusion_matrix_1x1(self) -> None:
        ExampleFactory.create(predictions={}, annotations={})
        matrix = confusion_matrix(Example.objects.all())
        self.assertEqual(len(matrix), 1)
        self.assertListEqual(
            matrix[0], [ColoredMatrixValue("None", "None", 100.0, primary_color)]
        )

    def test_confusion_matrix_2x2(self) -> None:
        for p in ["a", "b"]:
            for a in ["a", "b"]:
                ExampleFactory.create(
                    predictions={"label": p}, annotations={"label": a}
                )
        matrix = confusion_matrix(Example.objects.all())
        self.assertEqual(len(matrix), 2)
        self.assertListEqual(
            matrix[0],
            [
                ColoredMatrixValue(x="a", y="a", value=25.0, color=primary_color),
                ColoredMatrixValue(x="b", y="a", value=25.0, color=primary_color),
            ],
        )
        self.assertListEqual(
            matrix[1],
            [
                ColoredMatrixValue(x="a", y="b", value=25.0, color=primary_color),
                ColoredMatrixValue(x="b", y="b", value=25.0, color=primary_color),
            ],
        )
