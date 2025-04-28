from decimal import Decimal

from config import SYMBOL
from operations.ticks import get_ticks
from services.generate_id import generate_unique_id

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

    for i, tick in enumerate(ticks.itertuples(index=False)):
        tick_bid = Decimal(str(tick.bid))
        tick_ask = Decimal(str(tick.ask))

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
                if tick_ask < order["level_down"]:  # Cancel order
                    print("cancel order sell")
                    curr_order["price"] = tick_ask
                    canceled_orders.append(curr_order)
                    deferred_orders.remove(order)

                if tick_ask >= order["level_middle"]:  # Open order
                    print("open order sell")
                    curr_order["price"] = tick_ask
                    active_orders.append(curr_order)
                    opened_orders.append(curr_order)
                    deferred_orders.remove(order)

        for order in active_orders[:]:
            curr_order = order.copy()
            curr_order["time"] = candle["time"]

            if order["type"] == "BUY":
                if tick_bid < order["level_down"]:  # Stop loss
                    curr_order["profit"] = False
                    curr_order["price"] = tick_bid
                    closed_orders.append(curr_order)
                    active_orders.remove(order)

                if tick_bid >= order["level_up"]:  # Take profit
                    curr_order["profit"] = True
                    curr_order["price"] = tick_bid
                    closed_orders.append(curr_order)
                    active_orders.remove(order)

            elif order["type"] == "SELL":
                if tick_ask > order["level_up"]:  # Stop loss
                    curr_order["profit"] = False
                    curr_order["price"] = tick_ask
                    closed_orders.append(curr_order)
                    active_orders.remove(order)

                if tick_ask <= order["level_down"]:  # Take profit
                    curr_order["profit"] = True
                    curr_order["price"] = tick_ask
                    closed_orders.append(curr_order)
                    active_orders.remove(order)


def trade_by_trend_test(swings, df):
    level_up = 0
    level_down = 0
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
            global deferred_orders, start_deferre_orders

            if level_up == 0 or level_down == 0:
                return

            if swings[i]["count_candles"] == 2 or (
                swings[i]["count_candles"] == 1 and swings[i - 1]["count_candles"] >= 2
            ):
                # print(f"curr_idx: {i}, broke_idx: {broke_idx}")
                if broke_idx == i - 1:
                    level_middle = level_down + (level_up - level_down) * Decimal("0.5")
                    # print("level_middle:", level_middle)

                    if swings[i]["type"] == "UP":  # SWING LOW
                        if any(item["type"] == "SELL" for item in deferred_orders):
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
                        if any(item["type"] == "BUY" for item in deferred_orders):
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
                    broke_idx = i
                    # print("UP: ", i)
            else:  # DOWN
                if level_down == 0 or level_down > curr_level:  # Price broke line DOWN
                    level_down = curr_level
                    level_up = swings[i - 1]["level"]
                    broke_idx = i
                    # print("DOWN: ", i)


def get_orders():
    global canceled_orders, closed_orders, opened_orders, start_deferre_orders

    return canceled_orders, closed_orders, opened_orders, start_deferre_orders
