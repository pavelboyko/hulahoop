import logging
import math
from typing import Tuple, List, Dict, Generator
from dataclasses import dataclass
from itertools import groupby
from operator import itemgetter
from datetime import date
from datetime import timedelta
from django.db.models import QuerySet, Count
from matplotlib import cm, colors
from app.models import Example, Issue, Tag

logger = logging.getLogger(__package__)

colormap = "Blues"
primary_color = "#08306b"


@dataclass
class ColoredCounter:
    value: str
    count: int
    share: float  # in %
    color: str | None
    search: str | None = None


@dataclass
class ColoredMatrixValue:
    x: str
    y: str
    value: float | str  # in % or an empty string
    color: str | None
    search: str | None = None


ColoredMatrix = List[List[ColoredMatrixValue]]


def rgba_to_hex(rgba: Tuple[float, float, float, float]) -> str:
    return f"#{int(rgba[0] * 255):02x}{int(rgba[1] * 255):02x}{int(rgba[2] * 255):02x}"


def example_count(issue: Issue) -> int:
    return issue.example_set.filter().count()  # type: ignore


def example_count_daily(
    examples: QuerySet[Example], dayrange: Generator[date, None, None]
) -> Tuple[List[str], List[int]]:
    """
    :returns: list of days and list of example counts
    """
    sparse = (
        examples.values("created_at__date")
        .annotate(count=Count("id"))
        .values("created_at__date", "count")
        .order_by("created_at__date")
    )
    if not sparse:
        return [], []

    labels = list(dayrange)
    values = [0] * len(labels)
    for x in sparse:
        try:
            i = labels.index(x["created_at__date"])
            values[i] = x["count"]
        except ValueError as e:
            logger.warning(
                f"Can't find date {x['created_at__date']} in range {labels}: {e}. This is a bug."
            )

    str_labels = [day.strftime("%b %d") for day in labels]
    return str_labels, values


def tag_values_count(examples: QuerySet[Example]) -> Dict[str, List[ColoredCounter]]:
    """
    :returns: dict of tag name to list of (value, count, share) for every tag value, sorted by count descending
    """
    tag_count = list(
        Tag.objects.filter(example__in=examples)
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
            # 0.19 is an arbitraty factor here to make the colors look better
            color = rgba_to_hex(cmap(1 - math.modf(i * 0.19)[0]))
            out[key].append(
                ColoredCounter(
                    value=x["value"],
                    count=x["count"],
                    share=share * 100,
                    color=color,
                )
            )
    return out


def confusion_matrix(examples: QuerySet[Example]) -> ColoredMatrix:
    """
    :returns: list of matrix rows, where each row is a list of ColoredMatrixValue
    """

    def zero_to_empty(x) -> str:
        return x if x else ""

    sparse = (
        examples.values("annotations__label", "predictions__label")
        .annotate(count=Count("id"))
        .values_list("annotations__label", "predictions__label", "count")
    )
    value_norm = sum(x[2] for x in sparse)
    # combine annoated and predicted labels and convert to strings in the process
    labels = list(set(str(x[0]) for x in sparse).union(set(str(x[1]) for x in sparse)))
    if not labels:
        return []
    labels.sort()

    # prepare color palette
    cmap = cm.get_cmap(colormap)
    max_count = max(x[2] for x in sparse) / value_norm * 100
    color_norm = colors.Normalize(vmin=0, vmax=max_count)

    matrix = []
    for predicted in labels:
        row = []
        for annotated in labels:
            count = sum(
                x[2] / value_norm * 100
                for x in sparse
                if str(x[0]) == annotated and str(x[1]) == predicted
            )
            color = rgba_to_hex(cmap(color_norm(count))) if count > 0 else None
            row.append(
                ColoredMatrixValue(
                    x=annotated,
                    y=predicted,
                    value=zero_to_empty(count),
                    color=color,
                )
            )
        matrix.append(row)
    return matrix
