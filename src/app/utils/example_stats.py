import logging
import math
from typing import Tuple, List, Dict
from dataclasses import dataclass
from itertools import groupby
from operator import itemgetter
from django.utils import timezone
from datetime import timedelta
from django.db.models import QuerySet, Count
from matplotlib import cm, colors
from app.models import Example, Issue, Tag

logger = logging.getLogger(__package__)

colormap = "viridis"


@dataclass(frozen=True)
class ColoredCounter:
    value: str
    count: int
    share: float  # in %
    color: str | None


@dataclass(frozen=True)
class ColoredMatrixValue:
    x: str
    y: str
    value: str
    color: str | None


ColoredMatrix = List[List[ColoredMatrixValue]]


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


def issue_tag_values_count(issue: Issue) -> Dict[str, List[ColoredCounter]]:
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
    cmap = cm.get_cmap(colormap)
    out = {}
    for key, value in groupby(tag_count, itemgetter("key")):
        data = sorted(list(value), key=itemgetter("count"), reverse=True)
        norm = sum(x["count"] for x in data)
        out[key] = []
        for i, x in enumerate(data):
            share = x["count"] / norm
            rgba = cmap(math.modf(i * 0.29)[0])
            color = f"#{int(rgba[0] * 255):02x}{int(rgba[1] * 255):02x}{int(rgba[2] * 255):02x}"
            out[key].append(
                ColoredCounter(
                    value=x["value"],
                    count=x["count"],
                    share=share * 100,
                    color=color,
                )
            )
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


def examples_confusion_matrix2(examples: QuerySet[Example]) -> ColoredMatrix:
    """
    :returns: list of matrix rows, where each row is a list of ColoredMatrixValue
    """

    def zero_to_dash(x) -> str:
        return x if x else ""

    sparse = (
        examples.values("annotations__label", "predictions__label")
        .annotate(count=Count("id"))
        .values_list("annotations__label", "predictions__label", "count")
    )
    labels = list(
        set(str(x[0]) for x in sparse).union(set(str(x[1]) for x in sparse))
    )  # convert everything to str btw
    labels.sort()

    cmap = cm.get_cmap(colormap)
    max_count = max(x[2] for x in sparse)
    color_norm = colors.Normalize(vmin=0, vmax=max_count)  # TODO: check for None

    matrix = []
    for predicted in labels:
        row = []
        for annotated in labels:
            count = sum(
                x[2]
                for x in sparse
                if str(x[0]) == annotated and str(x[1]) == predicted
            )
            if count == 0:
                color = None
            else:
                rgba = cmap(color_norm(count))
                color = f"#{int(rgba[0] * 255):02x}{int(rgba[1] * 255):02x}{int(rgba[2] * 255):02x}"
            row.append(
                ColoredMatrixValue(
                    x=annotated,
                    y=predicted,
                    value=zero_to_dash(count),
                    color=color,
                )
            )
        matrix.append(row)
    return matrix
