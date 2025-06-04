from lightweight_charts import Chart
import pandas as pd

import finplot as fplt


def show_static_statistic(df, trend=None, markers=None, balance_history=None):

    # chart = Chart(toolbox=True)
    # chart.watermark("1")

    # chart.set(df)

    # trend_line = chart.create_line(
    #     name="trend", color="rgb(2, 199, 196)", price_label=True
    # )
    # trend_line.set(trend)

    # for i, row in enumerate(markers.itertuples(index=False)):
    #     chart.marker(
    #         time=row.time,
    #         shape=row.marker,
    #         color=row.color,
    #         text=row.text,
    #     )

    # balance_chart = chart.create_subchart(
    #     position="right", sync=True, height=1, width=0.5, toolbox=True
    # )
    # balance_chart.watermark("2")

    # balance_chart.set(df)

    # balance_line = balance_chart.create_line(
    #     name="trend",
    #     color="orange",
    # )

    # balance_line.set(trend)

    # chart.show(block=True)

    ax1 = fplt.create_plot("Main Chart", rows=2)
    fplt.candlestick_ochl(df)

    fplt.show()
