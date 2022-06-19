from app.models import Issue
from pyecharts.charts import Bar
from pyecharts.charts.chart import Chart
from pyecharts.globals import RenderType
from pyecharts import options as opts

echarts_host = "https://cdn.jsdelivr.net/npm/echarts@5.3.3/dist/"

colormap = [
    "#C1232B",
    "#27727B",
    "#FCCE10",
    "#E87C25",
    "#B5C334",
    "#FE8463",
    "#9BCA63",
    "#FAD860",
    "#F3A43B",
    "#60C0DD",
    "#D7504B",
    "#C6E579",
    "#F4E001",
    "#F0805A",
    "#26C0C0",
]


def plot_examples_last_n_days(issue: Issue, ndays: int = 30) -> Chart:
    labels, values = issue.example_count_last_n_days(ndays)
    chart = Bar(
        init_opts=opts.InitOpts(
            width="100%",
            height="200px",
            animation_opts=opts.AnimationOpts(animation=False),
            renderer=RenderType.SVG,
            theme="white",
        ),
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="shadow"),
        legend_opts=opts.LegendOpts(is_show=False),
        yaxis_opts=opts.AxisOpts(is_show=True),
    )
    chart.js_host = echarts_host
    chart.add_xaxis(labels)
    chart.add_yaxis(
        "Examples",
        values,
        stack="stack",
        label_opts=opts.LabelOpts(is_show=False),
    )

    return chart
