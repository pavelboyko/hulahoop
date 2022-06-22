import logging
from typing import Sequence, Tuple, List, Dict
from dataclasses import dataclass
from itertools import groupby
from operator import itemgetter
from django.utils import timezone
from datetime import timedelta
from django.db.models import QuerySet, Count
from app.models import Example, Issue, Tag

logger = logging.getLogger(__package__)


@dataclass(frozen=True)
class ValueCounter:
    value: str
    count: int
    share: float  # in %


def issue_example_count(issue: Issue) -> int:
    return issue.example_set.filter().count()  # type: ignore


def issue_example_count_last_n_days(
    issue: Issue, ndays: int = 30
) -> Tuple[List[str], List[int]]:
    """
    :returns: list of days and list of example counts
    """
    now = timezone.now()
    examples = (
        issue.example_set.filter(  # type: ignore
            created_at__gte=now - timedelta(days=ndays),
        )
        .values("created_at__date")
        .annotate(count=Count("id"))
        .values("created_at__date", "count")
        .order_by("created_at__date")
    )
    labels = [(now - timedelta(days=ndays - i)).strftime("%b %d") for i in range(ndays)]
    values = [0] * ndays
    for x in examples:
        values[(x["created_at__date"] - now.date()).days + ndays - 1] = x["count"]
    return labels, values


def issue_tag_values_count(issue: Issue) -> Dict[str, List[ValueCounter]]:
    """
    :returns: dict of tag name to list of (value, count, share) for every tag value, sorted by count descending
    """
    tag_count = list(
        Tag.objects.filter(example__issue=issue)
        .values("key", "value")
        .annotate(count=Count("id"))
        .values("key", "value", "count")
        .order_by("key")
    )
    out = {}
    for key, value in groupby(tag_count, itemgetter("key")):
        data = sorted(list(value), key=itemgetter("count"), reverse=True)
        norm = sum(x["count"] for x in data)
        out[key] = [
            ValueCounter(
                value=x["value"], count=x["count"], share=x["count"] * 100 / norm
            )
            for x in data
        ]
    return out


def examples_confusion_matrix(
    examples: QuerySet[Example],
) -> Tuple[List[str], List[Tuple[int, int, int]]]:
    """
    :returns: (list of labels, list of tuples (annotated_label_id, predicted_label_id, count))
    """
    cm = (
        examples.values("annotations__label", "predictions__label")
        .annotate(count=Count("id"))
        .values_list("annotations__label", "predictions__label", "count")
    )
    labels = list(
        set(str(x[0]) for x in cm).union(set(str(x[1]) for x in cm))
    )  # convert everything to str btw
    labels.sort()
    values = []
    for annotated_id, annotated in enumerate(labels):
        for predicted_id, predicted in enumerate(labels):
            values.append(
                (
                    annotated_id,
                    predicted_id,
                    sum(
                        x[2]
                        for x in cm
                        if str(x[0]) == annotated and str(x[1]) == predicted
                    ),
                )
            )
    return labels, values
