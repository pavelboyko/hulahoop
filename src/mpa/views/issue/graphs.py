from typing import Tuple, Sequence
from app.models import Issue
from pyecharts.charts import Bar, HeatMap
from pyecharts.charts.chart import Chart
from pyecharts.globals import RenderType
from pyecharts import options as opts
import random

echarts_host = "https://cdn.jsdelivr.net/npm/echarts@5.3.3/dist/"

colors = [
    "#2f4554",
    "#61a0a8",
    "#d48265",
    "#749f83",
    "#ca8622",
    "#bda29a",
    "#6e7074",
    "#546570",
    "#c4ccd3",
    "#f05b72",
    "#ef5b9c",
    "#f47920",
    "#905a3d",
    "#fab27b",
    "#2a5caa",
    "#444693",
    "#726930",
    "#b2d235",
    "#6d8346",
    "#ac6767",
    "#1d953f",
    "#6950a1",
    "#918597",
]


def plot_examples_last_n_days(labels: Sequence, values: Sequence) -> Chart:
    chart = Bar(
        init_opts=opts.InitOpts(
            width="300px",
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
        color=colors[0],
    )

    return chart


def plot_confusion_matrix(
    labels: Sequence[str], values: Sequence[Tuple[int, int, int]]
) -> Chart:
    """
    :param matrix: list of tuples (predicted, annotated, count)
    """

    chart = HeatMap(
        init_opts=opts.InitOpts(
            width="300px",
            height="370px",
            animation_opts=opts.AnimationOpts(animation=False),
            renderer=RenderType.SVG,
            theme="white",
        ),
    ).set_global_opts(
        visualmap_opts=opts.VisualMapOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(trigger="item", axis_pointer_type="shadow"),
        yaxis_opts=opts.AxisOpts(
            is_inverse=True,
            name="predicted",
            name_location="center",
            name_rotate=90,
            name_gap=20,
            type_="category",
        ),
        xaxis_opts=opts.AxisOpts(
            name="annotated",
            name_location="center",
            name_gap=20,
            type_="category",
        ),
    )
    chart.add_xaxis(labels)
    chart.add_yaxis(
        "",
        labels,  # type: ignore
        [x if x[2] != 0 else (x[0], x[1], "-") for x in values],  # type: ignore
        label_opts=opts.LabelOpts(is_show=True, position=""),
    )
    chart.js_host = echarts_host
    return chart
