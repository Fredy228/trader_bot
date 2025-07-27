from decimal import Decimal

from services.logger import logger
from database.types.orders import OrderDTO
from database.repository.orders import create_order, get_orders, update_order
from database.services.orders_service import open_order_event, cancel_order_event
from operations.ticks import get_ticks

from config import SYMBOL

last_tick = None


def trade_by_history_trend(level_up, level_down, candle, direction, is_change_trend):
    global last_tick
    time = candle["time"]

    if is_change_trend:
        is_buy = direction == "UP"
        level_middle = level_down + (level_up - level_down) * Decimal("0.5")

        def_ord: OrderDTO = {
            "type": "BUY" if is_buy else "SELL",
            "level_up": level_up,
            "level_down": level_down,
            "time": time.timestamp(),
            "price": level_middle,
            "status": "DEFERRED",
        }

        create_order(def_ord)
        logger.info(f"Створення відкладенного ордеру: {def_ord["type"]} {time}")

    deferred_orders = get_orders({"status": "DEFERRED"})
    active_orders = get_orders({"status": "OPENED"})

    if len(deferred_orders) == 0 and len(active_orders) == 0:
        return

    ticks = get_ticks(SYMBOL, time, candle["next_time"])

    if ticks is None:
        # Close all active orders if no ticks are available
        return

    for i, tick in enumerate(ticks.itertuples(index=False)):
        tick_bid = Decimal(str(tick.bid))
        tick_log_info = f"{tick_bid} {tick.time}"

        if i == len(ticks) - 1:
            last_tick = tick_bid

        for order in deferred_orders:
            curr_order = order.copy()
            curr_order["time"] = time
            curr_order["price"] = tick_bid

            is_buy = order["type"] == "BUY"
            is_sell = order["type"] == "SELL"

            # === UPDATE ORDER ===
            update_condition = (is_buy and tick_bid > order["level_up"]) or (
                is_sell and tick_bid < order["level_down"]
            )
            if update_condition:
                new_level_up = tick_bid if is_buy else order["level_up"]
                new_level_down = tick_bid if is_sell else order["level_down"]
                update_order(
                    order["id"],
                    {
                        "level_up": new_level_up,
                        "level_down": new_level_down,
                        "price": level_down + (level_up - level_down) * Decimal("0.5"),
                    },
                )
                logger.info(
                    f"Оновленно order {order['type']}_{order["id"]} {tick_log_info}"
                )
                continue

            # === OPEN ORDER ===
            open_condition = (is_buy and tick_bid <= order["price"]) or (
                is_sell and tick_bid >= order["price"]
            )
            if open_condition:
                curr_order["status"] = "OPENED"
                open_order_event(curr_order)
                logger.info(
                    f"Відкрито order {order['type']}_{order["id"]} {tick_log_info}"
                )
                continue

            # === CANCEL ORDER ===
            cancel_condition = (is_change_trend and is_buy and direction == "UP") or (
                is_change_trend and is_sell and direction == "DOWN"
            )
            if cancel_condition:
                cancel_order_event(curr_order)
                logger.info(
                    f"Скасовано order {order['type']}_{order["id"]} {tick_log_info}"
                )
                continue
