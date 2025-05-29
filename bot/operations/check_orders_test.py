from decimal import Decimal

from operations.ticks import get_ticks
from operations.transaction import transaction_test
from services.value_adjustment import value_adjustment
from operations.trade_by_history_trend import get_deferred_orders
from services.logger import logger

from config import SYMBOL, TAKE_PROFIT_DEVIATION, STOP_LOSS_DEVIATION, BREAK_TREND_BY

# IS_EXTREME = BREAK_TREND_BY == "extreme"

active_orders = []
canceled_orders = []
closed_orders = []
opened_orders = []

last_tick = None


def check_orders(from_time, to_time, candle):
    global active_orders, canceled_orders, closed_orders, opened_orders, last_tick

    deferred_orders = get_deferred_orders()

    if len(deferred_orders) == 0 and len(active_orders) == 0:
        return

    ticks = get_ticks(SYMBOL, from_time, to_time)

    if ticks is None:
        return

    for i, tick in enumerate(ticks.itertuples(index=False)):
        tick_bid = Decimal(str(tick.bid))
        tick_log_info = f"{tick_bid} {tick.time}"

        if i == len(ticks) - 1:
            last_tick = tick_bid

        for order in deferred_orders[:]:
            curr_order = order.copy()
            curr_order["time"] = from_time
            curr_order["price"] = tick_bid

            if order["type"] == "BUY":
                if tick_bid > order["level_up"]:  # Cancel order
                    logger.info(f"Відміненно order BUY {tick_log_info}")
                    canceled_orders.append(curr_order)
                    deferred_orders.remove(order)

                if tick_bid <= order["price"]:  # Open order
                    logger.info(f"Відкрито order BUY {tick_log_info}")
                    active_orders.append(curr_order)
                    opened_orders.append(curr_order)
                    deferred_orders.remove(order)

            elif order["type"] == "SELL":
                if tick_bid < order["level_down"]:  # Cancel order
                    logger.info(f"Відміненно order SELL {tick_log_info}")
                    canceled_orders.append(curr_order)
                    deferred_orders.remove(order)

                if tick_bid >= order["price"]:  # Open order
                    logger.info(f"Відкрито order SELL {tick_log_info}")
                    active_orders.append(curr_order)
                    opened_orders.append(curr_order)
                    deferred_orders.remove(order)

        for order in active_orders[:]:
            curr_order = order.copy()
            curr_order["time"] = from_time
            gap = order["level_up"] - order["level_down"]

            if order["type"] == "BUY":
                if tick_bid < order["level_down"] + value_adjustment(
                    STOP_LOSS_DEVIATION, gap
                ):  # Stop loss
                    curr_order["profit"] = False
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)

                    active_orders.remove(order)
                    logger.info(f"Stop loss order BUY {tick_log_info}")

                if tick_bid >= order["level_up"] + value_adjustment(
                    TAKE_PROFIT_DEVIATION, gap
                ):  # Take profit
                    curr_order["profit"] = True
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)
                    active_orders.remove(order)
                    logger.info(f"Take profit order BUY {tick_log_info}")

            elif order["type"] == "SELL":
                if tick_bid > order["level_up"] + value_adjustment(
                    STOP_LOSS_DEVIATION, gap, True
                ):  # Stop loss
                    curr_order["profit"] = False
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)
                    active_orders.remove(order)
                    logger.info(f"Stop loss order SELL {tick_log_info}")

                if tick_bid <= order["level_down"] + value_adjustment(
                    TAKE_PROFIT_DEVIATION, gap, True
                ):  # Take profit
                    curr_order["profit"] = True
                    curr_order["price"] = tick_bid
                    is_success = transaction_test(curr_order, order["price"])
                    if is_success:
                        closed_orders.append(curr_order)
                    else:
                        canceled_orders.append(curr_order)
                    active_orders.remove(order)
                    logger.info(f"Take profit order SELL {tick_log_info}")


def get_orders():
    global canceled_orders, closed_orders, opened_orders

    return canceled_orders, closed_orders, opened_orders


def close_active_orders(time):
    global last_tick, active_orders, closed_orders, canceled_orders

    if last_tick is None:
        return

    for order in active_orders[:]:
        curr_order = order.copy()
        curr_order["time"] = time
        curr_order["price"] = last_tick

        if order["type"] == "BUY":
            curr_order["profit"] = order["price"] < last_tick
            is_success = transaction_test(curr_order, order["price"])
            if is_success:
                closed_orders.append(curr_order)
            else:
                canceled_orders.append(curr_order)
        elif order["type"] == "SELL":
            curr_order["profit"] = order["price"] > last_tick
            is_success = transaction_test(curr_order, order["price"])
            if is_success:
                closed_orders.append(curr_order)
            else:
                canceled_orders.append(curr_order)

        active_orders.remove(order)
    logger.info(f"Закриття всіх ордерів")
