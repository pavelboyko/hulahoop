from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from app.models import Project, Issue
from .graphs import plot_examples_last_n_days


@login_required
def issue_detail(request, project_id, issue_id):
    project = get_object_or_404(Project, id=project_id)
    issue = get_object_or_404(Issue, id=issue_id, project=project)
    examples = issue.example_set.all().prefetch_related("attachment_set")  # type: ignore
    examples_last_30_days = plot_examples_last_n_days(issue, ndays=30)
    tag_count = issue.tag_values_count()

    paginator = Paginator(examples, 100)
    page_number = request.GET.get("page")

    return render(
        request,
        "mpa/issue/detail.html",
        {
            "project": project,
            "issue": issue,
            "examples_page": paginator.get_page(page_number),
            "examples_page_range": paginator.get_elided_page_range(
                page_number, on_each_side=1
            ),
            "examples_last_30_days": examples_last_30_days.render_embed(),
            "tag_count": tag_count,
        },
    )
