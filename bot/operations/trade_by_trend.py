from decimal import Decimal

from operations.ticks import get_ticks
from services.generate_id import generate_unique_id
from operations.transaction import transaction_test
from services.value_adjustment import value_adjustment

from config import SYMBOL, TAKE_PROFIT_DEVIATION, STOP_LOSS_DEVIATION

deferred_orders = []
active_orders = []

start_deferre_orders = []
canceled_orders = []
closed_orders = []
opened_orders = []


def check_orders(candle, prev_time):
    global deferred_orders, active_orders, canceled_orders, closed_orders, opened_orders

    if len(deferred_orders) == 0 and len(active_orders) == 0:
        return

    ticks = get_ticks(SYMBOL, candle["time"], prev_time)

    if ticks is None:
        return

    for i, tick in enumerate(ticks.itertuples(index=False)):
        tick_bid = Decimal(str(tick.bid))

        for order in deferred_orders[:]:
            curr_order = order.copy()
            curr_order["time"] = candle["time"]

            if order["type"] == "BUY":
                if tick_bid > order["level_up"]:  # Cancel order
                    print("cancel order buy")
                    curr_order["price"] = tick_bid
                    canceled_orders.append(curr_order)
                    deferred_orders.remove(order)

                if tick_bid <= order["level_middle"]:  # Open order
                    print("open order buy")
                    curr_order["price"] = tick_bid
                    active_orders.append(curr_order)
                    opened_orders.append(curr_order)
                    deferred_orders.remove(order)

            elif order["type"] == "SELL":
                if tick_bid < order["level_down"]:  # Cancel order
                    print("cancel order sell")
                    curr_order["price"] = tick_bid
                    canceled_orders.append(curr_order)
                    deferred_orders.remove(order)

                if tick_bid >= order["level_middle"]:  # Open order
                    print("open order sell")
                    curr_order["price"] = tick_bid
                    active_orders.append(curr_order)
                    opened_orders.append(curr_order)
                    deferred_orders.remove(order)

        for order in active_orders[:]:
            curr_order = order.copy()
            curr_order["time"] = candle["time"]

            if order["type"] == "BUY":
                if tick_bid < value_adjustment(
                    STOP_LOSS_DEVIATION, order["level_down"]
                ):  # Stop loss
                    curr_order["profit"] = False
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)

                    active_orders.remove(order)
                    print("Stop loss order buy")

                if tick_bid >= value_adjustment(
                    TAKE_PROFIT_DEVIATION, order["level_up"]
                ):  # Take profit
                    curr_order["profit"] = True
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)
                    active_orders.remove(order)
                    print("Take profit order buy")

            elif order["type"] == "SELL":
                if tick_bid > value_adjustment(
                    STOP_LOSS_DEVIATION, order["level_up"], True
                ):  # Stop loss
                    curr_order["profit"] = False
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)
                    active_orders.remove(order)
                    print("Stop loss order sell")

                if tick_bid <= value_adjustment(
                    TAKE_PROFIT_DEVIATION, order["level_down"], True
                ):  # Take profit
                    curr_order["profit"] = True
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)
                    active_orders.remove(order)
                    print("Take profit order sell")


def trade_by_trend_test(swings, df):
    level_up = 0
    level_down = 0
    current_trend = None
    broke_idx = None

    if len(swings) < 5:
        return

    for i in range(0, len(swings)):
        curr_level = swings[i]["level"]
        curr_time_start = swings[i]["time_start"]
        curr_time_end = swings[i]["time_end"]
        is_up = swings[i]["type"] == "UP"

        if i == 0:  # fist el
            if is_up:
                level_up = curr_level

            else:
                level_down = curr_level

        elif i == len(swings) - 1:  # last el
            # Logic for trade
            global deferred_orders, start_deferre_orders, active_orders

            if level_up == 0 or level_down == 0:
                return

            if (
                swings[i]["count_candles"] == 2 and swings[i - 1]["count_candles"] == 1
            ) or (
                swings[i]["count_candles"] == 1 and swings[i - 1]["count_candles"] >= 2
            ):
                if broke_idx == i - 1:
                    level_middle = level_down + (level_up - level_down) * Decimal("0.5")

                    if swings[i]["type"] == "UP":  # SWING LOW
                        if (
                            any(item["type"] == "SELL" for item in deferred_orders)
                            or any(item["type"] == "SELL" for item in active_orders)
                            or Decimal(str(df.iloc[len(df) - 2]["close"]))
                            > value_adjustment(STOP_LOSS_DEVIATION, level_up, True)
                        ):
                            return

                        def_ord = {
                            "type": "SELL",
                            "level_up": level_up,
                            "level_down": level_down,
                            "level_middle": level_middle,
                            "time": curr_time_end,
                            "price": level_middle,
                            "name": f"{generate_unique_id()}_sell",
                        }
                        deferred_orders.append(def_ord)
                        start_deferre_orders.append(def_ord)
                        print("deferred order sell")

                    else:  # SWING HIGH
                        if (
                            any(item["type"] == "BUY" for item in deferred_orders)
                            or any(item["type"] == "BUY" for item in active_orders)
                            or Decimal(str(df.iloc[len(df) - 2]["close"]))
                            < value_adjustment(STOP_LOSS_DEVIATION, level_down)
                        ):
                            return

                        def_ord = {
                            "type": "BUY",
                            "level_up": level_up,
                            "level_down": level_down,
                            "level_middle": level_middle,
                            "time": curr_time_end,
                            "price": level_middle,
                            "name": f"{generate_unique_id()}_buy",
                        }
                        deferred_orders.append(def_ord)
                        start_deferre_orders.append(def_ord)
                        print("deferred order buy")

            check_orders(df.iloc[len(df) - 1], df.iloc[len(df) - 2]["time"])

        else:  # middle el
            if is_up:  # UP
                if level_up == 0 or level_up < curr_level:  # Price broke line UP
                    level_up = curr_level
                    level_down = swings[i - 1]["level"]

                    if current_trend == "DOWN":
                        broke_idx = i

                    current_trend = "UP"

            else:  # DOWN
                if level_down == 0 or level_down > curr_level:  # Price broke line DOWN
                    level_down = curr_level
                    level_up = swings[i - 1]["level"]

                    if current_trend == "UP":
                        broke_idx = i

                    current_trend = "DOWN"


def get_orders():
    global canceled_orders, closed_orders, opened_orders, start_deferre_orders

    return canceled_orders, closed_orders, opened_orders, start_deferre_orders
