import MetaTrader5 as mt5
from pprint import pprint
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import signal
import sys

from common.connect import connect
from common.account import output_account_info
from operations.candles import get_candles
from operations.extremes import find_extremes
from operations.trend import plot_trend

from config import SYMBOL, BARS, TIMEFRAME, DEBUG_MODE

connect()


output_account_info()

app = dash.Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Graph(id="live-graph"),
        dcc.Interval(id="interval-component", interval=10000, n_intervals=0),
    ]
)


@app.callback(
    Output("live-graph", "figure"), Input("interval-component", "n_intervals")
)
def update_graphic(n):
    print("\nGetting data...\n")
    df = get_candles(SYMBOL, TIMEFRAME, BARS)
    if DEBUG_MODE == 1:
        print("candles:\n", df)

    print("\nFinding extremes...\n")
    swings = find_extremes(df=df)
    if DEBUG_MODE == 1:
        pprint(swings)

    print("\nTrend analysis...\n")
    hours_line, values_line = plot_trend(
        swings=swings, candle={"high": df["high"][0], "low": df["low"][0]}
    )

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["time"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
            )
        ]
    )

    fig.add_trace(
        go.Scatter(
            x=hours_line,
            y=values_line,
            mode="lines+markers",
            name="Трендовая линия",
            line=dict(color="red", width=2, dash="dash"),
        )
    )

    fig.update_layout(
        title=f"Анализ тренда: {SYMBOL}",
        xaxis_title="Время",
        yaxis_title="Цена",
        xaxis_rangeslider_visible=True,
    )

    return fig


def signal_handler(sig, frame):
    print("\n Программа остановливается... \nВыполняем отключение от Metatrader 5...")
    mt5.shutdown()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    app.run(debug=DEBUG_MODE == 1)
