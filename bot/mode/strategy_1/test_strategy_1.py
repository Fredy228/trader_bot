from pprint import pprint
import dash
from dash import html, dcc
import plotly.graph_objects as go
from decimal import Decimal

from operations.candles import get_candles_from_date
from operations.extremes import find_extremes
from operations.trade_by_trend import trade_by_trend_test, get_orders
from operations.trend import plot_trend
from operations.transaction import get_balance, get_time_line_balance

from config import (
    SYMBOL,
    TIMEFRAME,
    FROM_DATE,
    DEBUG_MODE,
    MODE,
    START_BALANCE,
    TAKE_PROFIT_DEVIATION,
    STOP_LOSS_DEVIATION,
    BREAK_TREND_BY,
)

app = dash.Dash(__name__)


def test_strategy_1():

    print("\nЙде отримання даних...\n")
    df = get_candles_from_date(SYMBOL, TIMEFRAME, FROM_DATE)
    len_df = len(df)
    print(f"Отримано {len_df} свічок\n")

    print("\nЙде торгівля...\n")
    for i in range(5, len_df):
        gap = df[0 : i + 1] if i <= 60 else df[i - 60 : i + 1]
        gap = gap.reset_index(drop=True)

        swings = find_extremes(df=gap)

        trade_by_trend_test(swings, gap)
        print(f"Прогрес {round((i / len_df) * 100)}%")

    print("\nЙде будування графіка...\n")
    canceled_orders, closed_orders, opened_orders, start_deferre_orders = get_orders()

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
            name="Трендова лінія",
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
                name=f"Відкладено: {trade['name']}<br>",
                hovertext=(
                    f"Відкладено: {trade['name']}<br>"
                    f"Значення: {trade['price']}<br>"
                    f"Верхня точка: {trade['level_up']}<br>"
                    f"Нижня точка: {trade['level_down']}<br>"
                    f"Час: {trade['time']}<br>"
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
                name=f"Відкрито: {trade["name"]}<br>",
                hovertext=(
                    f"Відкрито: {trade['name']}<br>"
                    f"Значення: {trade['price']}<br>"
                    f"Верхня точка: {trade['level_up']}<br>"
                    f"Нижня точка: {trade['level_down']}<br>"
                    f"Час: {trade['time']}<br>"
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
                name=f"{ f"Профіт: {trade["name"]}<br>"
                    if trade["profit"]
                    else f"Збиток: {trade["name"]}<br>"}",
                hovertext=(
                    f"{ f"Профіт: {trade["name"]}<br>"
                    if trade["profit"]
                    else f"Збиток: {trade["name"]}<br>"}"
                    f"Значення: {trade['price']}<br>"
                    f"Верхня точка: {trade['level_up']}<br>"
                    f"Нижня точка: {trade['level_down']}<br>"
                    f"Час: {trade['time']}<br>"
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
                name=f"Скасовано: {trade['name']}<br>",
                hovertext=(
                    f"Скасовано: {trade['name']}<br>"
                    f"Значення: {trade['price']}<br>"
                    f"Верхня точка: {trade['level_up']}<br>"
                    f"Нижня точка: {trade['level_down']}<br>"
                    f"Час: {trade['time']}<br>"
                ),
                hoverinfo="text",
            )
        )

    fig.update_layout(
        title=f"Торгівля",
        xaxis_title="Час",
        yaxis_title="Ціна",
        xaxis_rangeslider_visible=True,
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
        title=f"Історія балансу",
        xaxis_title="Час",
        yaxis_title="Баланс",
        xaxis_rangeslider_visible=True,
    )

    print("\nЗапуск вебсайту...\n")

    last_balance = get_balance()

    p_style = {"fontSize": 18, "margin": "0 0 3px 0"}

    app.layout = html.Div(
        [
            html.H1("Конфігурація", style={"textAlign": "center", "fontSize": 25}),
            html.Div(
                [
                    html.P(
                        f"Символ: {SYMBOL}",
                        style=p_style,
                    ),
                    html.P(
                        f"Таймфрейм: {TIMEFRAME}",
                        style=p_style,
                    ),
                    html.P(
                        f"Дата старту: {FROM_DATE}",
                        style=p_style,
                    ),
                    html.P(
                        f"Take profit deviation: {TAKE_PROFIT_DEVIATION}%",
                        style=p_style,
                    ),
                    html.P(
                        f"Stop loss deviation: {STOP_LOSS_DEVIATION}%",
                        style=p_style,
                    ),
                    html.P(
                        f"Break trend by: {BREAK_TREND_BY}",
                        style=p_style,
                    ),
                    html.P(
                        f"Режим: {MODE}", style={"fontSize": 18, "margin": "0 0 15px 0"}
                    ),
                    html.P(
                        f"Кількість свічок: {len_df}",
                        style={"fontSize": 18, "margin": "0 0 5px 0"},
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "flex-start",
                    "gap": "10px",
                    "marginBottom": "30px",
                    "padding": " 0 30px",
                },
            ),
            html.Div(
                [
                    dcc.Graph(figure=fig, style={"height": "90vh", "width": "100%"}),
                    dcc.Graph(figure=fig2, style={"height": "90vh", "width": "100%"}),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "gap": "20px",
                    "marginBottom": "30px",
                },
            ),
            html.H1("Підсумок", style={"textAlign": "center", "fontSize": 25}),
            html.Div(
                [
                    html.P(
                        f"Баланс: {START_BALANCE} => {last_balance}",
                        style=p_style,
                    ),
                    html.P(
                        f"{"Профіт" if last_balance >= Decimal(str(START_BALANCE)) else "Збиток"}: {last_balance - Decimal(str(START_BALANCE))}",
                        style=p_style,
                    ),
                    html.P(
                        f"Кількість відкрих угод:  {len(opened_orders)}",
                        style=p_style,
                    ),
                    html.P(
                        f"Кількість відхилених угод:  {len(canceled_orders)}",
                        style=p_style,
                    ),
                    html.P(
                        f"Кількість \u2191профіт\u2191 угод:  {sum(1 for order in closed_orders if order["profit"] is True)}",
                        style=p_style,
                    ),
                    html.P(
                        f"Кількість \u2193збиток\u2193 угод:  {sum(1 for order in closed_orders if order["profit"] is False)}",
                        style=p_style,
                    ),
                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "alignItems": "flex-start",
                    "gap": "10px",
                    "marginBottom": "30px",
                    "padding": " 0 30px",
                },
            ),
        ]
    )

    return app
