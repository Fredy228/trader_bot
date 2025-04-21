from decimal import Decimal

deferred_orders = []
active_orders = []
canceled_orders = []

# df.iloc[i]


def check_deferred_orders(candle):
    global deferred_orders, active_orders, canceled_orders
    for order in deferred_orders[:]:
        curr_order = order.copy()
        if order["type"] == "BUY":
            if (
                candle["high"] > order["level_up"]
                and candle["low"] > order["level_middle"]
            ):  # Cancel order
                deferred_orders.remove(order)
                curr_order["time"] = candle["time"]
                canceled_orders.append(curr_order)
        elif order["type"] == "SELL":
            print("SELL")


def trade_by_trend_test(swings, df):
    level_up = 0
    level_down = 0
    time_line = []
    values_line = []

    if len(swings) < 2:
        return

    for i in range(0, len(swings) - 1):
        curr_level = swings[i]["level"]
        curr_time_start = swings[i]["time_start"]
        curr_time_end = swings[i]["time_end"]
        curr_batch = swings[i]["bacth"]
        curr_indexes = swings[i]["indexes"]
        is_up = swings[i]["type"] == "UP"

        if i == 0:  # fist el
            if is_up:
                level_up = curr_level
                values_line.append(
                    df["low"][0] if swings[i]["count_candles"] > 1 else df["high"][0]
                )

            else:
                level_down = curr_level
                values_line.append(
                    df["high"][0] if swings[i]["count_candles"] > 1 else df["low"][0]
                )

            time_line.append(curr_time_start)
        elif i == len(swings) - 1:  # last el
            # Logic for trade
            global deferred_orders

            if swings[i]["count_candles"] == 2 or (
                swings[i]["count_candles"] == 1 and swings[i - 1]["count_candles"] >= 2
            ):
                level_middle = level_down + (level_up - level_down) * Decimal("0.5")
                if swings[i]["type"] == "UP":  # SWING LOW
                    if swings[i - 1]["level"] < level_down:  # Price broke line DOWN
                        deferred_orders.append(
                            {
                                "type": "SELL",
                                "level_up": level_up,
                                "level_down": level_down,
                                "level_middle": level_middle,
                                "time": curr_time_end,
                            }
                        )
                        print()
                else:  # SWING HIGH
                    if swings[i - 1]["level"] > level_up:  # Price broke line UP
                        deferred_orders.append(
                            {
                                "type": "BUY",
                                "level_up": level_up,
                                "level_down": level_down,
                                "level_middle": level_middle,
                                "time": curr_time_end,
                            }
                        )
                        print()

        else:  # middle el
            if is_up:  # UP
                if level_up == 0 or level_up < curr_level:  # Price broke line UP
                    time_line.append(curr_time_end)
                    values_line.append(curr_level)
                    level_up = curr_level
                    level_down = swings[i - 1]["level"]
            else:  # DOWN
                if level_down == 0 or level_down > curr_level:  # Price broke line DOWN
                    time_line.append(curr_time_end)
                    values_line.append(curr_level)
                    level_down = curr_level
                    level_up = swings[i - 1]["level"]
