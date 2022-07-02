import django_filters
from django import forms
from crispy_forms.helper import FormHelper
from app.models import Project


class ProjectFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr="icontains",
        label="",
        widget=forms.TextInput(
            attrs={
                "type": "search",
                "autocomplete": "off",
                "placeholder": "Search projects",
                # submit form on input clear
                "oninput": "if (this.value.length == 0) { this.form.submit() }",
            }
        ),
    )
    is_archived = django_filters.BooleanFilter(
        label="Show archived",
        widget=forms.CheckboxInput(
            attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked"}
        ),
    )
    order = django_filters.OrderingFilter(
        choices=(
            ("-updated_at", "Last updated"),
            ("name", "Name"),
            ("-issues", "Issues"),
        ),
        label="",
        empty_label=None,
        null_label=None,
    )

    class Meta:
        model = Project
        fields = ["name", "is_archived"]

    def __init__(self, data, *args, **kwargs):
        if not data.get("order"):
            data = data.copy()
            data["order"] = "-updated_at"

        super().__init__(data, *args, **kwargs)
        self.form.helper = FormHelper()
        self.form.helper.form_method = "get"
        # self.form.helper.form_show_labels = True
        for _, field in self.form.fields.items():
            field.widget.attrs.update({"onchange": "this.form.submit()"})
