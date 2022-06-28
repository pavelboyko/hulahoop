from django.test import TestCase
from app.models import Example, Tag
from app.fixtures import ExampleFactory
from app.utils.example_search import (
    ExampleSearchQuery,
    KV,
    parse_query_string,
    query_to_Q,
    query_to_string,
    ParsingError,
)


class Test(TestCase):
    """
    ./manage.py test app.utils.tests.test_example_search.Test --keepdb --verbosity 2
    """

    def tearDown(self) -> None:
        Example.objects.all().delete()

    def test_parse_invalid(self) -> None:
        invalid_queries = [
            None,
            "a",
            "a b",
            "a = b",
            "a=b c",
            "tags__a=b",
            "random=qqq",
            "qqq=qqq",  # unknown field
            "random=0",
            "random=-1",
            '"',
            'a="b" "',
        ]
        for q in invalid_queries:
            print(q)
            self.assertRaises(ParsingError, parse_query_string, q)

    def test_parse_tag(self) -> None:
        query = parse_query_string("tag__a=b")
        self.assertEqual(len(query.tags), 1)
        self.assertEqual(query.tags[0].key, "a")
        self.assertEqual(query.tags[0].value, "b")

    def test_parse_field(self) -> None:
        query = parse_query_string("fingerprint=qqq")
        self.assertEqual(len(query.fields), 1)
        self.assertEqual(query.fields[0].key, "fingerprint")
        self.assertEqual(query.fields[0].value, "qqq")

    def test_parse_field_subfield(self) -> None:
        query = parse_query_string("annotations__label=qqq")
        self.assertEqual(len(query.fields), 1)
        self.assertEqual(query.fields[0].key, "annotations__label")
        self.assertEqual(query.fields[0].value, "qqq")

    def test_parse_field_subsubfield(self) -> None:
        query = parse_query_string("annotations__choices__0=qqq")
        self.assertEqual(len(query.fields), 1)
        self.assertEqual(query.fields[0].key, "annotations__choices__0")
        self.assertEqual(query.fields[0].value, "qqq")

    def test_parse_random(self) -> None:
        query = parse_query_string("random=100")
        self.assertEqual(query.random, 100)

    def test_parse_whitespace_value(self) -> None:
        query = parse_query_string('tag__a="x y"')
        self.assertEqual(len(query.tags), 1)
        self.assertEqual(query.tags[0].key, "a")
        self.assertEqual(query.tags[0].value, "x y")

    def test_parse_whitespace_key(self) -> None:
        query = parse_query_string('"tag__a b"=c')
        self.assertEqual(len(query.tags), 1)
        self.assertEqual(query.tags[0].key, "a b")
        self.assertEqual(query.tags[0].value, "c")

    def test_str_empty(self) -> None:
        query = ExampleSearchQuery([], [])
        self.assertEqual(query_to_string(query), "")

    def test_str(self) -> None:
        query = ExampleSearchQuery(
            tags=[KV("a", "b"), KV("c", "d")],
            fields=[KV("annotations", "qqq"), KV("predictions", "ppp")],
            random=100,
        )
        self.assertEqual(
            query_to_string(query),
            "annotations=qqq predictions=ppp tag__a=b tag__c=d random=100",
        )

    def test_str_whitespace(self) -> None:
        query = ExampleSearchQuery(
            tags=[KV("a", "x y"), KV("b", "x y z")],
            fields=[KV("annotations", "xxx yyy"), KV("predictions", "xxx yyy zzz")],
        )
        self.assertEqual(
            query_to_string(query),
            'annotations="xxx yyy" predictions="xxx yyy zzz" tag__a="x y" tag__b="x y z"',
        )

    def test_Q_tags(self) -> None:
        ex1: Example = ExampleFactory.create(tags=0)
        Tag.objects.create(example=ex1, key="a", value="b")
        ExampleFactory(tags=0)
        query = ExampleSearchQuery(tags=[KV("a", "b")], fields=[])
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].id, ex1.id)

    def test_Q_fields(self) -> None:
        ex1: Example = ExampleFactory.create(tags=0, fingerprint="qqq")
        ExampleFactory(tags=0, fingerprint="ppp")
        query = ExampleSearchQuery(tags=[], fields=[KV("fingerprint", "qqq")])
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].id, ex1.id)
