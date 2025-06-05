from lightweight_charts import Chart
import pandas as pd
from flask import Flask, send_file, jsonify
import os

# import finplot as fplt

app = Flask(__name__)


def show_static_statistic(df, trend=None, markers=None, balance_history=None):
    print("Statustic")
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

    # ax1 = fplt.create_plot("Main Chart", rows=2)
    # fplt.candlestick_ochl(df)

    # fplt.show()

    @app.route("/")
    def index():
        path = os.path.join(os.getcwd(), "bot", "static", "index.html")
        return send_file(path)

    @app.route("/data")
    def get_data():
        candles = [
            {
                "time": int(row["time"].timestamp()),
                "open": row["open"],
                "high": row["high"],
                "low": row["low"],
                "close": row["close"],
            }
            for _, row in df.iterrows()
        ]

        trend_js = [
            {
                "time": int(row["time"].timestamp()),
                "value": row["trend"],
            }
            for _, row in trend.iterrows()
        ]

        markers_js = [
            {
                "time": int(row["time"].timestamp()),
                "color": row["color"],
                "shape": row["marker"],
                "text": row["text"],
                "position": row["position"],
            }
            for _, row in markers.iterrows()
        ]

        return jsonify({"candles": candles, "trend": trend_js, "markers": markers_js})

    app.run(port=8080, debug=False, host="0.0.0.0")
