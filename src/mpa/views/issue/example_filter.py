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
from app.utils.date_ranges import date_ranges

logger = logging.getLogger(__package__)


class ExampleFilter(django_filters.FilterSet):
    timestamp = django_filters.DateRangeFilter(
        field_name="timestamp",
        label="Example timestamp",
        empty_label=None,
        choices=[(key, value["label"]) for key, value in date_ranges.items()],
        filters={key: value["filter"] for key, value in date_ranges.items()},
    )
    search = django_filters.CharFilter(
        label="Search",
        method="do_search",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "class": "search form-control ms-1",
                "autocomplete": "off",
                "placeholder": "Search examples by tags, predictions, annotations, and metadata",
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
            return qs
        except ParsingError as e:
            self.search_error_message = f"{e}"
            logger.error(self.search_error_message)
            return queryset.none()

    class Meta:
        model = Example
        fields = ["timestamp"]

    def __init__(self, data, *args, **kwargs):
        if not data.get("timestamp"):
            data = data.copy()
            data["timestamp"] = "month"

        super().__init__(data, *args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
        self.form.helper.form_show_labels = False
        for _, field in self.form.fields.items():
            field.widget.attrs.update({"onchange": "this.form.submit()"})
