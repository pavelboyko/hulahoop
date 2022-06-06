from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from app.models import Project, Example
from pyecharts.charts import Bar
from pyecharts.charts.chart import Chart
from pyecharts.globals import RenderType
from pyecharts import options as opts

colors = [
    "#DD5703",
    "#cccccc",
    "#215DE8",
    "#129504",
    "#BD1498",
    "#E50400",
]


def plot_examples_last_n_days(project: Project, ndays: int = 30) -> Chart:
    now = timezone.now()
    examples = (
        Example.objects.filter(
            project=project,
            is_deleted=False,
            created_at__gte=now - timedelta(days=ndays),
        )
        .values("created_at__date", "status")
        .annotate(count=Count("id"))
        .values("created_at__date", "status", "count")
        .order_by("created_at__date")
    )
    chart = (
        Bar(
            init_opts=opts.InitOpts(
                width="100%",
                height="320px",
                animation_opts=opts.AnimationOpts(animation=False),
                renderer=RenderType.SVG,
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
        )
        .set_colors(colors)
    )
    labels = [(now - timedelta(days=ndays - i)).strftime("%b %d") for i in range(ndays)]
    values = {status.value: [0] * ndays for status in Example.Status}
    for x in examples:
        values[x["status"]][(x["created_at__date"] - now.date()).days + ndays - 1] = x[
            "count"
        ]
    chart.add_xaxis(labels)
    for key, value in values.items():
        chart.add_yaxis(
            Example.Status(key).name,
            value,
            stack="stack",
            label_opts=opts.LabelOpts(is_show=False),
        )

    return chart


@login_required
def project_dashboard(request, project_id):
    project = get_object_or_404(Project, id=project_id, is_deleted=False)
    examples_last_n_days = plot_examples_last_n_days(project, ndays=30)
    return render(
        request,
        "mpa/project/dashboard.html",
        {
            "project": project,
            "examples_last_n_days": examples_last_n_days.render_embed(),
        },
    )
