from pprint import pprint
import plotly.graph_objects as go

from operations.candles import get_candles
from operations.extremes import find_extremes
from operations.trend import plot_trend

from config import SYMBOL, BARS, TIMEFRAME, DEBUG_MODE


def test_strategy_1():
    print("\nИдет получение данных...\n")
    df = get_candles(SYMBOL, TIMEFRAME, BARS)
    if DEBUG_MODE == 1:
        print("candles:\n", df)

    print("\nПоиск экстремумов...\n")
    swings = find_extremes(df=df)
    if DEBUG_MODE == 1:
        pprint(swings)

    print("\nПостроение тренда...\n")
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
            line=dict(color="red", width=2, dash="solid"),
        )
    )

    fig.update_layout(
        title=f"Анализ тренда: {SYMBOL}",
        xaxis_title="Время",
        yaxis_title="Цена",
        xaxis_rangeslider_visible=True,
    )
