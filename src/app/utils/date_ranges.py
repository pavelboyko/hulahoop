from datetime import timedelta
from django.utils.timezone import now


def _truncate(dt):
    return dt.date()


date_ranges = {
    "today": {
        "label": "Today",
        "filter": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: now().year,
                "%s__month" % name: now().month,
                "%s__day" % name: now().day,
            }
        ),
        "dayrange": lambda: [_truncate(now())],
    },
    "yesterday": {
        "label": "Yesterday",
        "filter": lambda qs, name: qs.filter(
            **{
                "%s__year" % name: (now() - timedelta(days=1)).year,
                "%s__month" % name: (now() - timedelta(days=1)).month,
                "%s__day" % name: (now() - timedelta(days=1)).day,
            }
        ),
        "dayrange": lambda: [_truncate(now() - timedelta(days=1))],
    },
    "week": {
        "label": "Last 7 days",
        "filter": lambda qs, name: qs.filter(
            **{
                "%s__gte" % name: _truncate(now() - timedelta(days=7)),
                "%s__lt" % name: _truncate(now()),
            }
        ),
        "dayrange": lambda: (
            _truncate(now() - timedelta(days=(7 - x))) for x in range(7)
        ),
    },
    "month": {
        "label": "Last 30 days",
        "filter": lambda qs, name: qs.filter(
            **{
                "%s__gte" % name: _truncate(now() - timedelta(days=30)),
                "%s__lt" % name: _truncate(now()),
            }
        ),
        "dayrange": lambda: (
            _truncate(now() - timedelta(days=(30 - x))) for x in range(30)
        ),
    },
    "quarter": {
        "label": "Last 90 days",
        "filter": lambda qs, name: qs.filter(
            **{
                "%s__gte" % name: _truncate(now() - timedelta(days=90)),
                "%s__lt" % name: _truncate(now()),
            }
        ),
        "dayrange": lambda: (
            _truncate(now() - timedelta(days=(90 - x))) for x in range(90)
        ),
    },
    "year": {
        "label": "Last 12 months",
        "filter": lambda qs, name: qs.filter(
            **{
                "%s__gte" % name: _truncate(now() - timedelta(days=365)),
                "%s__lt" % name: _truncate(now()),
            }
        ),
        "dayrange": lambda: (
            _truncate(now() - timedelta(days=(365 - x))) for x in range(365)
        ),
    },
}
