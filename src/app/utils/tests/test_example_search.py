from django.test import TestCase
from app.models import Example, Tag
from app.fixtures import ExampleFactory
from app.utils.example_search import (
    ExampleSearchQuery,
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
        self.assertDictEqual(query.tags, {"a": "b"})

    def test_parse_field(self) -> None:
        query = parse_query_string("fingerprint=qqq")
        self.assertDictEqual(query.fields, {"fingerprint": "qqq"})

    def test_parse_field_subfield(self) -> None:
        query = parse_query_string("annotations__label=qqq")
        self.assertDictEqual(query.fields, {"annotations__label": "qqq"})

    def test_parse_field_subsubfield(self) -> None:
        query = parse_query_string("annotations__choices__0=qqq")
        self.assertDictEqual(query.fields, {"annotations__choices__0": "qqq"})

    def test_parse_random(self) -> None:
        query = parse_query_string("random=100")
        self.assertEqual(query.random, 100)

    def test_parse_whitespace_value(self) -> None:
        query = parse_query_string('tag__a="x y"')
        self.assertDictEqual(query.tags, {"a": "x y"})

    def test_parse_whitespace_key(self) -> None:
        query = parse_query_string('"tag__a b"=c')
        self.assertDictEqual(query.tags, {"a b": "c"})

    def test_parse_double(self) -> None:
        query = parse_query_string("tag__a=b tag__a=c")
        self.assertDictEqual(query.tags, {"a": "c"})

    def test_str_empty(self) -> None:
        query = ExampleSearchQuery({}, {})
        self.assertEqual(query_to_string(query), "")

    def test_str(self) -> None:
        query = ExampleSearchQuery(
            tags={"a": "b", "c": "d"},
            fields={"fingerprint": "qqq", "predictions": "ppp"},
            random=100,
        )
        self.assertEqual(
            query_to_string(query),
            "fingerprint=qqq predictions=ppp tag__a=b tag__c=d random=100",
        )

    def test_str_whitespace(self) -> None:
        query = ExampleSearchQuery(
            tags={"a": "x y", "b": "x y z"},
            fields={"annotations": "xxx yyy", "predictions": "xxx yyy zzz"},
        )
        self.assertEqual(
            query_to_string(query),
            'annotations="xxx yyy" predictions="xxx yyy zzz" tag__a="x y" tag__b="x y z"',
        )

    def test_Q_tags(self) -> None:
        ex1: Example = ExampleFactory.create(tags=0)
        Tag.objects.create(example=ex1, key="a", value="b")
        ExampleFactory(tags=0)
        query = ExampleSearchQuery(tags={"a": "b"}, fields={})
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].id, ex1.id)

    def test_Q_fields(self) -> None:
        ex1: Example = ExampleFactory.create(tags=0, fingerprint="qqq")
        ExampleFactory(tags=0, fingerprint="ppp")
        query = ExampleSearchQuery(tags={}, fields={"fingerprint": "qqq"})
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)
        self.assertEqual(qs[0].id, ex1.id)

    def test_Q_fields_json(self) -> None:
        ExampleFactory.create(tags=0, predictions={"label": "a"})
        query = ExampleSearchQuery(tags={}, fields={"predictions__label": "a"})
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)

    def test_Q_fields_json_empty(self) -> None:
        ExampleFactory.create(tags=0, predictions=None)
        query = ExampleSearchQuery(tags={}, fields={"predictions__label": "None"})
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)

    def test_Q_fields_json_no_value(self) -> None:
        ExampleFactory.create(tags=0, predictions={"a": "b"})
        query = ExampleSearchQuery(tags={}, fields={"predictions__label": "None"})
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)

    def test_Q_fields_json_null_value(self) -> None:
        ExampleFactory.create(tags=0, predictions={"label": None})
        query = ExampleSearchQuery(tags={}, fields={"predictions__label": "None"})
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)

    def test_Q_fields_json_none_value(self) -> None:
        ExampleFactory.create(tags=0, predictions={"label": "None"})
        query = ExampleSearchQuery(tags={}, fields={"predictions__label": "None"})
        qs = Example.objects.filter(query_to_Q(query))
        self.assertEqual(qs.count(), 1)
