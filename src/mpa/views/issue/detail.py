import logging
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
import django_filters
from django import forms
from crispy_forms.helper import FormHelper
from django.core.paginator import Paginator
from app.models import Project, Issue, Example, Tag
from app.utils.example_stats import (
    confusion_matrix,
    tag_values_count,
    example_count_daily,
)
from .graphs import plot_examples_last_n_days

logger = logging.getLogger(__package__)


def parse_search_query(query: str) -> Q:
    """
    Parse a search query string into a list of search terms.
    """
    logger.debug(query)
    terms = query.split()
    q = Q()
    for term in terms:
        logger.debug(f"term: {term}")
        tokens = term.split("=")
        if len(tokens) != 2:
            logger.warning(
                f"Invalid search query term: {term}. Valid terms must be of the form 'key=value'."
            )
            continue
        if tokens[0][:4] == "tag:":
            logger.debug(f"Searching for tag: key={tokens[0][4:]} value={tokens[1]}")
            q = q & Q(tag__key=tokens[0][4:], tag__value=tokens[1])
        else:
            logger.debug(f"Searching for field: name={tokens[0]} value={tokens[1]}")
            q = q & Q(**{tokens[0]: tokens[1]})
    return q


class ExampleFilter(django_filters.FilterSet):
    created_at = django_filters.DateRangeFilter(
        field_name="created_at", label="Example timestamp"
    )
    search = django_filters.CharFilter(
        label="Search",
        method="do_search",
        widget=forms.TextInput(
            attrs={
                "id": "search",
                "class": "search form-control ms-1",
                "autocomplete": "off",
                "placeholder": "Filter examples...",
            }
        ),
    )

    def do_search(self, queryset, name, value):
        return queryset.filter(parse_search_query(value))

    class Meta:
        model = Example
        fields = ["created_at"]

    def __init__(self, data, *args, **kwargs):
        if not data.get("created_at"):
            data = data.copy()
            data["created_at"] = "week"

        super().__init__(data, *args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
        self.form.helper.form_show_labels = False
        for _, field in self.form.fields.items():
            field.widget.attrs.update({"onchange": "this.form.submit()"})


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
    confusion_matrix2 = confusion_matrix(filter.qs)  # type: ignore

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
            "confusion_matrix2": confusion_matrix2,
        },
    )
