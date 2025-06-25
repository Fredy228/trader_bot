from flask import Flask, send_file, jsonify
import os
import threading

from services.open_web import open_browser

app = Flask(__name__)


def show_static_statistic(df, trend=None, markers=None, balance_history=None):

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

        balance_js = [
            {
                "time": int(row["time"].timestamp()),
                "value": row["value"],
            }
            for _, row in balance_history.iterrows()
        ]

        return jsonify(
            {
                "candles": candles,
                "trend": trend_js,
                "markers": markers_js,
                "balance": balance_js,
            }
        )

    threading.Thread(target=open_browser).start()
    app.run(port=8080, debug=False, host="0.0.0.0")
