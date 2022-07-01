import django_filters
from django import forms
from crispy_forms.helper import FormHelper
from app.models import Issue


class IssueFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="Search issues",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "autocomplete": "off",
                # submit form on input clear
                "oninput": "if (this.value.length == 0) { this.form.submit() }",
            }
        ),
    )
    status = django_filters.ChoiceFilter(
        choices=Issue.Status.choices, empty_label="All"
    )
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
