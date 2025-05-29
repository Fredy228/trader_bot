from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.layouts import column
from bokeh.models import WheelZoomTool


def show_static_statistic(df, trend=None, markers=None, balance_history=None):

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
        title="Trade",
        # sizing_mode="stretch_both",
        sizing_mode="stretch_width",
        height=400,
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

    if markers:
        marker_source = ColumnDataSource(
            data=dict(
                time=markers["time"],
                price=list(map(float, markers["price"])),
                label=markers["name"],
                color=markers["color"],
                marker=markers["marker"],
            )
        )

        marker_renderer = p.scatter(
            x="time",
            y="price",
            size=30,
            color="color",
            marker="marker",
            source=marker_source,
            legend_field="label",
            line_width=2,
            line_color="black",
        )

        marker_hover = HoverTool(
            renderers=[marker_renderer],
            tooltips=[
                ("Тип", "@label"),
                ("Цена", "@price"),
                ("Время", "@time{%F %H:%M}"),
            ],
            formatters={"@time": "datetime"},
        )

        p.add_tools(marker_hover)

    if balance_history:
        balance_source = ColumnDataSource(
            data=dict(
                time=balance_history["time"],
                balance=list(map(float, balance_history["balance"])),
            )
        )

        balance_plot = figure(
            x_axis_type="datetime",
            title="Баланс",
            sizing_mode="stretch_width",
            height=320,
            x_range=p.x_range,
        )

        balance_plot.line(
            x="time",
            y="balance",
            source=balance_source,
            line_color="orange",
            line_width=2,
        )

        balance_plot.yaxis.axis_label = "Баланс"
        balance_plot.xaxis.axis_label = "Час"
    else:
        balance_plot = None

    p.grid.grid_line_alpha = 0.6
    p.yaxis.axis_label = "Ціна"
    p.xaxis.axis_label = "Час"

    if balance_plot:
        show(column(p, balance_plot, sizing_mode="stretch_both"))
    else:
        show(p)
