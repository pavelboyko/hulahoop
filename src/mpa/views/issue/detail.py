from typing import Dict, List, Any
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app.models import Project, Issue
from app.utils.example_stats import (
    examples_confusion_matrix,
    issue_tag_values_count,
    issue_example_count,
    issue_example_count_last_n_days,
)
from .graphs import plot_confusion_matrix, plot_examples_last_n_days, colors


def colored_tag_count(issue: Issue) -> Dict[str, List[Dict[str, Any]]]:
    out = {}
    for key, stats in issue_tag_values_count(issue).items():
        out[key] = []
        for i, data in enumerate(stats):
            out[key].append(
                {
                    "value": data.value,
                    "share": data.share,
                    "color": colors[i % len(colors)],
                }
            )
    return out


@login_required
def issue_detail(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id)
    issue = get_object_or_404(Issue, id=issue_id, project=project)
    examples = issue.example_set.all().prefetch_related("attachment_set", "tag_set")  # type: ignore

    paginator = Paginator(examples, 100)
    page_number = request.GET.get("page", 1)

    example_count = issue_example_count(issue)
    ex30_labels, ex30_values = issue_example_count_last_n_days(issue, 30)
    examples_last_30_days = plot_examples_last_n_days(
        ex30_labels, ex30_values
    ).render_embed()
    tag_count = colored_tag_count(issue)
    cm_labels, cm_values = examples_confusion_matrix(examples)
    confusion_matrix = plot_confusion_matrix(cm_labels, cm_values).render_embed()

    return render(
        request,
        "mpa/issue/detail.html",
        {
            "project": project,
            "issue": issue,
            "examples_page": paginator.get_page(page_number),
            "example_count": example_count,
            "examples_last_30_days": examples_last_30_days,
            "tag_count": tag_count,
            "confusion_matrix": confusion_matrix,
        },
    )
