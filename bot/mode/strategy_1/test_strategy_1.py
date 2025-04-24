from pprint import pprint
import plotly.graph_objects as go

from operations.candles import get_candles_from_date
from operations.extremes import find_extremes
from operations.trade_by_trend import trade_by_trend_test, get_orders
from operations.trend import plot_trend

from config import SYMBOL, TIMEFRAME, FROM_DATE, DEBUG_MODE


def test_strategy_1():

    print("\nИдет получение данных...\n")
    df = get_candles_from_date(SYMBOL, TIMEFRAME, FROM_DATE)
    if DEBUG_MODE == 1:
        print("candles:\n", df)

    print("\nИдет торговля...\n")
    for i in range(2, len(df)):
        gap = df[0 : i + 1] if i <= 60 else df[i - 60 : i + 1]
        gap = gap.reset_index(drop=True)

        swings = find_extremes(df=gap)

        trade_by_trend_test(swings, gap)

        # print(gap.iloc[len(gap) - 1])

    print("\nИдет постройка графика...\n")
    canceled_orders, closed_orders = get_orders()

    print("\nЗакрытые ордера:\n")
    pprint(closed_orders)

    print("\nОтмененные ордера:\n")
    pprint(canceled_orders)

    hours_line, values_line = plot_trend(
        swings=swings,
        candle={"high": df["high"][0], "low": df["low"][0], "time": df["time"][0]},
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
            line=dict(color="yellow", width=2, dash="solid"),
        )
    )

    for trade in closed_orders:
        fig.add_trace(
            go.Scatter(
                x=[trade["time"]],
                y=[trade["price"]],
                mode="markers",
                marker=dict(
                    color="green" if trade["profit"] else "red",
                    size=14,
                    symbol="triangle-up" if trade["profit"] else "triangle-down",
                    line=dict(width=1, color="black"),
                ),
                name="Профит" if trade["profit"] else "Убыток",
            )
        )

    for trade in canceled_orders:
        fig.add_trace(
            go.Scatter(
                x=[trade["time"]],
                y=[trade["price"]],
                mode="markers",
                marker=dict(
                    color="blue", size=14, symbol="x", line=dict(width=1, color="black")
                ),
                name="Отменено",
            )
        )

    fig.update_layout(
        title=f"Торговля: {SYMBOL}",
        xaxis_title="Время",
        yaxis_title="Цена",
        xaxis_rangeslider_visible=True,
    )

    fig.show()

    print("\nГотово\n")
