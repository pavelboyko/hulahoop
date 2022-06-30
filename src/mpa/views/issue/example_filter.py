import logging
import django_filters
from django import forms
from crispy_forms.helper import FormHelper
from app.models import Example
from app.utils.example_search import (
    ExampleSearchQuery,
    parse_query_string,
    query_to_Q,
    ParsingError,
)

logger = logging.getLogger(__package__)


class ExampleFilter(django_filters.FilterSet):
    created_at = django_filters.DateRangeFilter(
        field_name="created_at", label="Example timestamp"
    )
    search = django_filters.CharFilter(
        label="Search",
        method="do_search",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "class": "search form-control ms-1",
                "autocomplete": "off",
                "placeholder": "Search examples by tags, predictions, annotations, and metadata...",
                # submit form on input clear
                "oninput": "if (this.value.length == 0) { this.form.submit() }",
            }
        ),
    )
    search_query: ExampleSearchQuery | None = None
    search_error_message: str | None = None

    def do_search(self, queryset, name, value):
        self.search_error_message = None
        self.search_query = None
        try:
            self.search_query = parse_query_string(value)
            qs = queryset.filter(query_to_Q(self.search_query))
            if self.search_query.random is not None:
                qs = qs.order_by("?")[: self.search_query.random]
            return qs
        except ParsingError as e:
            self.search_error_message = f"{e}"
            logger.error(self.search_error_message)
            return queryset.none()

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
