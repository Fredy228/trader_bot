from flask import Flask, send_file, jsonify
import os
import threading

from services.open_web import open_browser

app = Flask(__name__)


def show_static_statistic(df, trend=None, markers=None, balance_history=None):

    orders_js = dict()
    for order in markers:
        saved_order = orders_js.get(order["id_order"], {})

        is_open = order["status"] == "OPENED"
        is_closed = order["status"] == "CLOSED"

        if is_closed:
            saved_order["profit"] = order["profit"]

        if is_open or is_closed:
            saved_order["type"] = order["type"]
            saved_order["openPrice" if is_open else "closePrice"] = order["price"]
            saved_order["openTime" if is_open else "closeTime"] = order["time"]
            orders_js[order["id_order"]] = saved_order

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

    balance_js = [
        {
            "time": row["time"],
            "value": row["value"],
        }
        for _, row in balance_history.iterrows()
    ]

    @app.route("/")
    def index():
        path = os.path.join(os.getcwd(), "bot", "static", "index.html")
        return send_file(path)

    @app.route("/data")
    def get_data():

        return jsonify(
            {
                "candles": candles,
                "trend": trend_js,
                "orders": sorted(
                    orders_js.values(), key=lambda o: o.get("openTime", float("inf"))
                ),
                "balance": balance_js,
            }
        )

    threading.Thread(target=open_browser).start()
    app.run(port=8080, debug=False, host="0.0.0.0")
