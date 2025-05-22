import dash
from dash import html, dcc
import plotly.graph_objects as go

from bokeh.plotting import figure, show, output_file
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import layout
from bokeh.io import curdoc
from bokeh.models import WheelZoomTool

app = dash.Dash(__name__)


def show_static_statistic(df, trend=None):

    df["color"] = [
        "green" if close > open_ else "red"
        for close, open_ in zip(df["close"], df["open"])
    ]

    source = ColumnDataSource(
        data=dict(
            time=df["time"],
            open=df["open"],
            close=df["close"],
            high=df["high"],
            low=df["low"],
            color=df["color"],
        )
    )

    p = figure(
        x_axis_type="datetime",
        title="Candlestick Chart",
        sizing_mode="stretch_both",
    )

    wheel_zoom = WheelZoomTool(dimensions="both", zoom_on_axis=True)
    wheel_zoom.speed = 0.05

    p.add_tools(wheel_zoom)
    p.toolbar.active_scroll = wheel_zoom

    p.segment(x0="time", y0="high", x1="time", y1="low", color="color", source=source)
    vbar = p.vbar(
        x="time",
        width=3_000_000,  # ширина в микросекундах
        top="open",
        bottom="close",
        fill_color="color",
        line_color="color",
        source=source,
    )

    hover = HoverTool(
        renderers=[vbar],
        tooltips=[
            ("Время", "@time{%F %H:%M}"),
            ("Open", "@open"),
            ("High", "@high"),
            ("Low", "@low"),
            ("Close", "@close"),
        ],
        formatters={"@time": "datetime"},
        mode="vline",
    )

    p.add_tools(hover)

    if trend:
        p.line(
            x=trend["time"],
            y=list(map(float, trend["line"])),
            line_color="rgb(2, 199, 196)",
            line_width=3,
            line_dash="solid",
            legend_label="Тренд",
        )

    p.grid.grid_line_alpha = 0.6
    p.yaxis.axis_label = "Ціна"
    p.xaxis.axis_label = "Час"

    show(p)
