import django_filters
from django import forms
from crispy_forms.helper import FormHelper
from app.models import Issue


class IssueFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Search issues by name",
        widget=forms.TextInput(attrs={"class": "search", "autocomplete": "off"}),
    )
    status = django_filters.ChoiceFilter(choices=Issue.Status.choices)
    examples__gte = django_filters.NumberFilter(
        field_name="examples", lookup_expr="gte", label="Min examples"
    )
    order = django_filters.OrderingFilter(
        choices=(
            ("-examples", "Examples"),
            ("-last_seen", "Last seen"),
            ("-first_seen", "First seen"),
        ),
        label="Sort by",
        empty_label=None,
        null_label=None,
    )

    class Meta:
        model = Issue
        fields = ["name", "status"]

    def __init__(self, data, *args, **kwargs):
        if not data.get("order"):
            data = data.copy()
            data["order"] = "-examples"

        super().__init__(data, *args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
        self.form.helper.label_class = "text-muted"
        for _, field in self.form.fields.items():
            field.widget.attrs.update({"onchange": "this.form.submit()"})
