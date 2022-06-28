from django.http import QueryDict
from django import template

register = template.Library()


@register.simple_tag
def query_string(*args, **kwargs):
    """
    Combines dictionaries of query parameters and individual query parameters
    and builds an encoded URL query string from the result.
    Taken from https://code.djangoproject.com/ticket/10941

    Usage examples:
    {# Just repeat the parameters: #}
    {% query_string request.GET %}

    {# Add a parameter: #}
    {% query_string request.GET format='pdf' %}

    {# Change a parameter: #}
    {% query_string request.GET page=next_page_number %}

    {# Overwrite month and year with precomputed values, e.g. with next_month_year = {'month': 1, 'year': 2022}, and clear the day: #}
    {% query_string request.GET next_month_year day=None %}
    """
    query_dict = QueryDict(mutable=True)

    for a in args:
        query_dict.update(a)

    remove_keys = []

    for k, v in kwargs.items():
        if v is None:
            remove_keys.append(k)
        elif isinstance(v, list):
            query_dict.setlist(k, v)
        else:
            query_dict[k] = v

    for k in remove_keys:
        if k in query_dict:
            del query_dict[k]

    qs = query_dict.urlencode()
    if not qs:
        return ""
    return "?" + qs
