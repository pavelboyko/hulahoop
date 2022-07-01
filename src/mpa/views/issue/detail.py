from cmath import e
import logging
import copy
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app.models import Project, Issue
from app.utils.example_stats import (
    confusion_matrix,
    tag_values_count,
    example_count_daily,
)
from app.utils.example_search import ExampleSearchQuery, query_to_string
from app.utils.date_ranges import date_ranges
from .graphs import plot_example_count_daily
from .example_filter import ExampleFilter
from .export import export_json

logger = logging.getLogger(__package__)


def copy_query(query):
    return copy.deepcopy(query) if query is not None else ExampleSearchQuery({}, {})


@login_required
def issue_detail(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id)
    issue = get_object_or_404(Issue, id=issue_id, project=project)
    examples = (
        issue.example_set.all()  # type: ignore
        .order_by("-created_at")
        .prefetch_related("attachment_set", "tag_set")
    )

    filter = ExampleFilter(request.GET, queryset=examples)

    daily_count_labels, daily_count_values = example_count_daily(
        filter.qs,  # type: ignore
        date_ranges[request.GET.get("created_at", "week")]["dayrange"](),
    )
    daily_count_graph = plot_example_count_daily(daily_count_labels, daily_count_values)

    tag_count = tag_values_count(filter.qs)  # type: ignore
    for key, data in tag_count.items():
        for tag in data:
            query = copy_query(filter.search_query)
            query.tags[key] = tag.value
            tag.search = query_to_string(query)

    cm = confusion_matrix(filter.qs)  # type: ignore
    for row in cm:
        for cell in row:
            query = copy_query(filter.search_query)
            query.fields["annotations__label"] = cell.x
            query.fields["predictions__label"] = cell.y
            cell.search = query_to_string(query)

    rquery = copy_query(filter.search_query)
    if rquery.random is None:
        rquery.random = 5
    random_search = query_to_string(rquery)

    if filter.search_query is not None and filter.search_query.random is not None:
        examples_to_display = filter.qs.order_by("?")[: filter.search_query.random]
    else:
        examples_to_display = filter.qs

    count = examples_to_display.count()

    if "export" in request.GET:
        return export_json(examples_to_display.iterator(), count)  # type: ignore

    paginator = Paginator(examples_to_display, 100)
    page_number = request.GET.get("page", 1)

    return render(
        request,
        "mpa/issue/detail.html",
        {
            "project": project,
            "issue": issue,
            "filter": filter,
            "examples_page": paginator.get_page(page_number),
            "example_count": count,
            "examples_last_30_days": daily_count_graph,
            "tag_count": tag_count,
            "confusion_matrix": cm,
            "random_search": random_search,
        },
    )
