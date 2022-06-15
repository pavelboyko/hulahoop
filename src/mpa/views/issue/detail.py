from itertools import groupby
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from app.models import Project, Issue, ExampleTag
from .graphs import plot_examples_last_n_days


def get_tag_count(issue: Issue):
    tag_count = list(
        ExampleTag.objects.filter(example__issue=issue)
        .values("key", "value")
        .annotate(count=Count("id"))
        .values("key", "value", "count")
        .order_by("key")
    )
    return {key: list(value) for key, value in groupby(tag_count, lambda x: x["key"])}


@login_required
def issue_detail(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id)
    issue = get_object_or_404(Issue, id=issue_id, project=project)
    examples = issue.example_set.all()
    examples_last_30_days = plot_examples_last_n_days(issue, ndays=30)
    tag_count = get_tag_count(issue)
    return render(
        request,
        "mpa/issue/detail.html",
        {
            "project": project,
            "issue": issue,
            "examples": examples,
            "examples_last_30_days": examples_last_30_days.render_embed(),
            "tag_count": tag_count,
        },
    )
