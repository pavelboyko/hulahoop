import logging
from typing import List, Tuple, Dict
from dataclasses import dataclass
from itertools import groupby
from operator import itemgetter
from django.utils import timezone
from datetime import timedelta
from django.db import models
from django.contrib import admin

from app.models.example import Example
from .base import BaseModel, BaseAdmin
from .tag import Tag

logger = logging.getLogger(__package__)


class Issue(BaseModel):
    """
    A group of similar Examples
    """

    class Status(models.IntegerChoices):
        open = 0
        muted = 10
        resolved = 20  # a resolved Issue can receive new Examples and reopen
        closed = 30  # a closed Issue can not receive new Examples

    project: models.ForeignKey = models.ForeignKey(
        "Project", null=False, blank=False, on_delete=models.CASCADE
    )
    status: models.IntegerField = models.IntegerField(
        choices=Status.choices, default=Status.open
    )
    name: models.TextField = models.TextField(null=True, blank=True)
    fingerprint: models.TextField = models.TextField(
        null=True, blank=True, default=None
    )
    first_seen: models.DateTimeField = models.DateTimeField(
        default=timezone.now,
        null=True,
    )
    last_seen: models.DateTimeField = models.DateTimeField(
        default=timezone.now,
        null=True,
    )

    def __str__(self) -> str:
        return f"#{self.id}"  # type: ignore

    def add_example(self, example: Example) -> None:
        example.issue = self
        example.save(update_fields=["issue"])
        if example.created_at < self.first_seen:
            self.first_seen = example.created_at
            self.save(update_fields=["first_seen"])
        if example.created_at > self.last_seen:
            self.last_seen = example.created_at
            self.save(update_fields=["last_seen"])
        # TODO: reopen resolved issue here?

    def example_count(self) -> int:
        return self.example_set.filter().count()  # type: ignore

    def example_count_last_n_days(self, ndays: int = 30) -> Tuple[List[str], List[int]]:
        now = timezone.now()
        examples = (
            self.example_set.filter(  # type: ignore
                created_at__gte=now - timedelta(days=ndays),
            )
            .values("created_at__date")
            .annotate(count=models.Count("id"))
            .values("created_at__date", "count")
            .order_by("created_at__date")
        )
        labels = [
            (now - timedelta(days=ndays - i)).strftime("%b %d") for i in range(ndays)
        ]
        values = [0] * ndays
        for x in examples:
            values[(x["created_at__date"] - now.date()).days + ndays - 1] = x["count"]
        return labels, values

    @dataclass
    class ValueCounter:
        value: str
        count: int
        share: float
        color: str

    def tag_values_count(self) -> Dict[str, List[ValueCounter]]:
        tag_count = list(
            Tag.objects.filter(example__issue=self)
            .values("key", "value")
            .annotate(count=models.Count("id"))
            .values("key", "value", "count")
            .order_by("key")
        )
        out = {}
        for key, value in groupby(tag_count, itemgetter("key")):
            data = sorted(list(value), key=itemgetter("count"), reverse=True)
            norm = sum(x["count"] for x in data)
            out[key] = [
                Issue.ValueCounter(
                    value=x["value"],
                    count=x["count"],
                    share=x["count"] * 100 / norm,
                    color="",  # to be determined later
                )
                for x in data
            ]
        return out


class IssueAdmin(BaseAdmin):
    readonly_fields = (
        "id",
        "created_at",
        "updated_at",
    )
    list_display = (
        "id",
        "project",
        "name",
        "status",
    )
    fields = (
        "id",
        "project",
        "name",
        "status",
        "created_at",
        "updated_at",
    )


admin.site.register(Issue, IssueAdmin)
