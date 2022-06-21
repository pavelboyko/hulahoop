from django.test import TestCase
from app.models import Project
from app.fixtures import ExampleFactory, IssueFactory
from app.models import Attachment, Tag


class Test(TestCase):
    """
    ./manage.py test app.fixtures.tests.test_example_factory.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Project.objects.all().delete()

    def test_without_issue(self) -> None:
        example = ExampleFactory()
        self.assertIsNotNone(example.project)
        self.assertIsNone(example.issue)

    def test_with_issue(self) -> None:
        issue = IssueFactory()
        example = ExampleFactory(project=issue.project, issue=issue)
        self.assertIsNotNone(example.project)
        self.assertIsNotNone(example.issue)
        self.assertEqual(example.project, issue.project)

    def test_with_one_attachment(self) -> None:
        example = ExampleFactory()
        self.assertEqual(example.attachment_set.count(), 1)  # type: ignore
        attachment: Attachment = example.attachment_set.first()  # type: ignore
        self.assertEqual(attachment.example, example)
        self.assertEqual(attachment.type, Attachment.Type.image)
        self.assertIsNotNone(attachment.url)

    def test_with_ten_attachments(self) -> None:
        example = ExampleFactory(attachments=10)
        self.assertEqual(example.attachment_set.count(), 10)  # type: ignore

    def test_without_attachments(self) -> None:
        example = ExampleFactory(attachments=0)
        self.assertEqual(example.attachment_set.count(), 0)  # type: ignore

    def test_with_one_tag(self) -> None:
        example = ExampleFactory()
        self.assertEqual(example.tag_set.count(), 2)  # type: ignore
        tag: Tag = example.tag_set.first()  # type: ignore
        self.assertEqual(tag.example, example)
        self.assertIsNotNone(tag.key)
        self.assertIsNotNone(tag.value)

    def test_with_ten_tags(self) -> None:
        example = ExampleFactory(tags=10)
        self.assertEqual(example.tag_set.count(), 11)  # type: ignore

    def test_without_tags(self) -> None:
        example = ExampleFactory(tags=0)
        self.assertEqual(example.tag_set.count(), 1)  # type: ignore
