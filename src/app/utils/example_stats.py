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

colormap = "Blues"
primary_color = "#08306b"


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
    value: float | str  # in % or an empty string
    color: str | None


ColoredMatrix = List[List[ColoredMatrixValue]]


def rgba_to_hex(rgba: Tuple[float, float, float, float]) -> str:
    return f"#{int(rgba[0] * 255):02x}{int(rgba[1] * 255):02x}{int(rgba[2] * 255):02x}"


def example_count(issue: Issue) -> int:
    return issue.example_set.filter().count()  # type: ignore


def example_count_last_n_days(
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


def tag_values_count(issue: Issue) -> Dict[str, List[ColoredCounter]]:
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
