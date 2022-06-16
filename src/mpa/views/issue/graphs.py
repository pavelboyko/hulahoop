from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from app.models import Issue, Example
from pyecharts.charts import Bar
from pyecharts.charts.chart import Chart
from pyecharts.globals import RenderType
from pyecharts import options as opts

echarts_host = "https://cdn.jsdelivr.net/npm/echarts@5.3.3/dist/"

colors = [
    "#DD5703",
    "#cccccc",
    "#215DE8",
    "#129504",
    "#BD1498",
    "#E50400",
]


def plot_examples_last_n_days(issue: Issue, ndays: int = 30) -> Chart:
    now = timezone.now()
    examples = (
        Example.objects.filter(
            issue=issue,
            created_at__gte=now - timedelta(days=ndays),
        )
        .values("created_at__date", "status")
        .annotate(count=Count("id"))
        .values("created_at__date", "status", "count")
        .order_by("created_at__date")
    )
    labels = [(now - timedelta(days=ndays - i)).strftime("%b %d") for i in range(ndays)]
    values = {status.value: [0] * ndays for status in Example.Status}
    for x in examples:
        values[x["status"]][(x["created_at__date"] - now.date()).days + ndays - 1] = x[
            "count"
        ]

    chart = (
        Bar(
            init_opts=opts.InitOpts(
                width="100%",
                height="200px",
                animation_opts=opts.AnimationOpts(animation=False),
                renderer=RenderType.SVG,
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
            legend_opts=opts.LegendOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(is_show=True),
        )
        .set_colors(colors)
    )
    chart.js_host = echarts_host
    chart.add_xaxis(labels)
    for key, value in values.items():
        chart.add_yaxis(
            Example.Status(key).name,
            value,
            stack="stack",
            label_opts=opts.LabelOpts(is_show=False),
        )

    return chart
