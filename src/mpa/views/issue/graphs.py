from typing import Tuple, Sequence
from app.models import Issue
from pyecharts.charts import Bar, HeatMap
from pyecharts.charts.chart import Chart
from pyecharts.globals import RenderType
from pyecharts import options as opts
from app.utils.example_stats import primary_color

echarts_host = "https://cdn.jsdelivr.net/npm/echarts@5.3.3/dist/"


def plot_example_count_daily(labels: Sequence, values: Sequence) -> str:
    chart = Bar(
        init_opts=opts.InitOpts(
            width="300px",
            height="200px",
            animation_opts=opts.AnimationOpts(animation=False),
            renderer=RenderType.SVG,
            theme="white",
        ),
    ).set_global_opts(
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="shadow",
            background_color="black",
            textstyle_opts=opts.TextStyleOpts(color="white"),
        ),
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
        color=primary_color,
    )

    return chart.render_embed()
