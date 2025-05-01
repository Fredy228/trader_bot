from pprint import pprint
import dash
from dash import html, dcc
import plotly.graph_objects as go

from operations.candles import get_candles_from_date
from operations.extremes import find_extremes
from operations.trade_by_trend import trade_by_trend_test, get_orders
from operations.trend import plot_trend
from operations.transaction import get_balance, get_time_line_balance

from config import SYMBOL, TIMEFRAME, FROM_DATE, DEBUG_MODE

app = dash.Dash(__name__)


def test_strategy_1():

    print("\nИдет получение данных...\n")
    df = get_candles_from_date(SYMBOL, TIMEFRAME, FROM_DATE)
    if DEBUG_MODE == 1:
        print("candles:\n", df)

    print("\nИдет торговля...\n")
    for i in range(5, len(df)):
        gap = df[0 : i + 1] if i <= 60 else df[i - 60 : i + 1]
        gap = gap.reset_index(drop=True)

        swings = find_extremes(df=gap)

        trade_by_trend_test(swings, gap)

        # print(gap.iloc[len(gap) - 1])

    print("\nИдет постройка графика...\n")
    canceled_orders, closed_orders, opened_orders, start_deferre_orders = get_orders()

    if DEBUG_MODE == 1:
        print("\Точка открытия ордера:\n")
        pprint(opened_orders)

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

    for trade in start_deferre_orders:
        fig.add_trace(
            go.Scatter(
                x=[trade["time"]],
                y=[trade["price"]],
                mode="markers",
                marker=dict(
                    color="rgb(128, 0, 128)",
                    size=14,
                    symbol="square",
                    line=dict(width=1, color="black"),
                ),
                name=f"Отложенно: {trade['name']}",
                hovertext=(
                    f"Отложенно: {trade['name']}<br>"
                    f"value: {trade['price']}<br>"
                    f"level_up: {trade['level_up']}<br>"
                    f"level_down: {trade['level_down']}<br>"
                    f"time: {trade['time']}<br>"
                ),
                hoverinfo="text",
            )
        )

    for trade in opened_orders:
        fig.add_trace(
            go.Scatter(
                x=[trade["time"]],
                y=[trade["price"]],
                mode="markers",
                marker=dict(
                    color="orange",
                    size=14,
                    symbol="arrow-bar-right",
                    line=dict(width=1, color="black"),
                ),
                name=f"Открыто: {trade['name']}",
                hovertext=(
                    f"Открыто: {trade['name']}<br>"
                    f"value: {trade['price']}<br>"
                    f"level_up: {trade['level_up']}<br>"
                    f"level_down: {trade['level_down']}<br>"
                    f"time: {trade['time']}<br>"
                ),
                hoverinfo="text",
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
                name=(
                    f"Профит: {trade["name"]}"
                    if trade["profit"]
                    else f"Убыток: {trade["name"]}"
                ),
                hovertext=(
                    f"{ f"Профит: {trade["name"]}<br>"
                    if trade["profit"]
                    else f"Убыток: {trade["name"]}<br>"}"
                    f"value: {trade['price']}<br>"
                    f"level_up: {trade['level_up']}<br>"
                    f"level_down: {trade['level_down']}<br>"
                    f"time: {trade['time']}<br>"
                ),
                hoverinfo="text",
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
                name=f"Отменено: {trade['name']}",
                hovertext=(
                    f"Отменено: {trade['name']}<br>"
                    f"value: {trade['price']}<br>"
                    f"level_up: {trade['level_up']}<br>"
                    f"level_down: {trade['level_down']}<br>"
                    f"time: {trade['time']}<br>"
                ),
                hoverinfo="text",
            )
        )

    fig.update_layout(
        title=f"Торговля: {SYMBOL}",
        xaxis_title="Время",
        yaxis_title="Цена",
        xaxis_rangeslider_visible=True,
        # dragmode="zoom",
        # yaxis=dict(fixedrange=False),
    )

    time_line_balabce, balance_line = get_time_line_balance()

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=time_line_balabce,
            y=balance_line,
            mode="lines+markers",
            name="Баланс",
            line=dict(color="red", width=2, dash="solid"),
            text=[
                "Баланс на " + str(t) + " =  " + str(b)
                for t, b in zip(time_line_balabce, balance_line)
            ],
            hoverinfo="text",
        )
    )

    fig2.update_layout(
        title=f"История баланса: {SYMBOL}",
        xaxis_title="Время",
        yaxis_title="Баланс",
        xaxis_rangeslider_visible=True,
    )

    print(f"\nИтоговый баланс: {get_balance()}\n")

    print("\nЗапуск сайта...\n")

    app.layout = html.Div(
        [
            html.Div(
                [
                    dcc.Graph(figure=fig, style={"height": "90vh", "width": "100%"}),
                    dcc.Graph(figure=fig2, style={"height": "90vh", "width": "100%"}),
                ],
                style={"display": "flex", "flexDirection": "column", "gap": "20px"},
            )
        ]
    )

    return app
