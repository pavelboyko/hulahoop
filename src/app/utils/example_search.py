import logging
from typing import List
from dataclasses import dataclass
import shlex
from django.db.models import Q
from app.models import Example, Tag


logger = logging.getLogger(__package__)


@dataclass(frozen=True)
class KV:
    key: str
    value: str


@dataclass(frozen=True)
class ExampleSearchQuery:
    tags: List[KV]
    fields: List[KV]
    random: int | None = None


class ParsingError(Exception):
    pass


def parse_query_string(query: str) -> ExampleSearchQuery:
    allowed_fields = [
        "fingerprint",
        "predictions",
        "annotations",
        "metadata",
        "created_at",
        "updated_at",
    ]
    if query is None:
        raise ParsingError("Query string is None")

    try:
        terms = shlex.split(query)
    except ValueError as e:
        raise ParsingError(f"Failed to parse query string: {e}") from e

    tags = []
    fields = []
    random = None

    for term in terms:
        tokens = term.split("=", 1)
        if len(tokens) != 2:
            raise ParsingError(f"Invalid search query: {term}. Expected key=value.")

        if tokens[0][:5] == "tag__":
            tags.append(KV(tokens[0][5:], tokens[1]))
        elif tokens[0] == "random":
            try:
                random = int(tokens[1])
            except ValueError as e:
                raise ParsingError(
                    f"Invalid search query: {term}. Expected random=<int>."
                ) from e
            if random <= 0:
                raise ParsingError(
                    f"Invalid search query: {term}. Expected random > 0."
                )
        else:
            key_parts = tokens[0].split("__")
            if key_parts[0] not in allowed_fields:
                raise ParsingError(
                    f"Invalid search query: {term}. Uknown field {tokens[0]}."
                )
            fields.append(KV(tokens[0], tokens[1]))

    return ExampleSearchQuery(tags, fields, random)


def query_to_Q(query: ExampleSearchQuery) -> Q:
    q = Q()
    for field in query.fields:
        q = q & Q(**{field.key: field.value})

    for tag in query.tags:
        q = q & Q(tag__key=tag.key, tag__value=tag.value)

    return q


def query_to_string(query: ExampleSearchQuery) -> str:
    def q(s: str) -> str:
        return f'"{s}"' if " " in s else s

    return " ".join(
        [f"{q(field.key)}={q(field.value)}" for field in query.fields]
        + [f"tag__{q(tag.key)}={q(tag.value)}" for tag in query.tags]
        + [f"random={query.random}" if query.random is not None else ""]
    ).strip()
