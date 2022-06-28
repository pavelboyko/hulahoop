import logging
import copy
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
from .graphs import plot_examples_last_n_days
from .example_filter import ExampleFilter

logger = logging.getLogger(__package__)


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
    paginator = Paginator(filter.qs, 100)
    page_number = request.GET.get("page", 1)

    count = filter.qs.count()
    daily_count_labels, daily_count_values = example_count_daily(
        filter.qs  # type: ignore
    )
    daily_count_graph = plot_examples_last_n_days(
        daily_count_labels, daily_count_values
    ).render_embed()
    tag_count = tag_values_count(filter.qs)  # type: ignore
    for key, data in tag_count.items():
        for tag in data:
            query = (
                copy.deepcopy(filter.search_query)
                if filter.search_query is not None
                else ExampleSearchQuery({}, {})
            )
            query.tags[key] = tag.value
            tag.search = query_to_string(query)

    cm = confusion_matrix(filter.qs)  # type: ignore
    for row in cm:
        for cell in row:
            query = (
                copy.deepcopy(filter.search_query)
                if filter.search_query is not None
                else ExampleSearchQuery({}, {})
            )
            query.fields["annotations__label"] = cell.x
            query.fields["predictions__label"] = cell.y
            cell.search = query_to_string(query)
            logger.debug(f"{cell.x} {cell.y} {cell.search}")

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
        },
    )
