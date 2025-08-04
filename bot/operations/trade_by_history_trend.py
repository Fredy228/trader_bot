from decimal import Decimal

from services.logger import logger
from database.types.orders import OrderDTO
from database.repository.orders import (
    create_order,
    get_orders,
    update_order,
    delete_order,
)
from database.services.orders_service import (
    open_order_event,
    cancel_order_event,
    close_order_event,
)
from operations.ticks import get_ticks
from operations.transaction import transaction_test
from services.round_decimal import round_decimal

from config import SYMBOL

last_tick = None


def trade_by_history_trend(
    level_up, level_down, candle, direction, is_change_trend, is_continue_trend
):
    global last_tick
    time = candle["time"]
    candle_info = f"Candle: open: {candle['open']}, close: {candle['close']}, high: {candle['high']}, low: {candle['low']} {time}"

    deferred_orders = get_orders({"status": "DEFERRED"})
    active_orders = get_orders({"status": "OPENED"})

    if is_continue_trend:
        for order in deferred_orders:
            curr_order = order.copy()
            curr_order["level_up"] = Decimal(str(order["level_up"]))
            curr_order["level_down"] = Decimal(str(order["level_down"]))

            is_buy = order["type"] == "BUY"
            is_sell = order["type"] == "SELL"
            #  UPDATE ORDER
            update_condition = (
                is_buy and direction == "UP" and level_up > curr_order["level_up"]
            ) or (
                is_sell
                and direction == "DOWN"
                and level_down < curr_order["level_down"]
            )
            if update_condition:
                new_level_up = level_up if is_buy else curr_order["level_up"]
                new_level_down = level_down if is_sell else curr_order["level_down"]
                update_order(
                    order["id"],
                    {
                        "level_up": str(new_level_up),
                        "level_down": str(new_level_down),
                        "price": str(
                            new_level_down
                            + (new_level_up - new_level_down) * Decimal("0.5")
                        ),
                    },
                )
                logger.info(
                    f"Оновленно order: {order['type']}_{order["id"]}, TP: {new_level_up if is_buy else new_level_down}, SL: {new_level_down if is_buy else new_level_up}, {time}"
                )

    if is_change_trend:
        is_buy = direction == "UP"
        level_middle = level_down + (level_up - level_down) * Decimal("0.5")

        def_ord: OrderDTO = {
            "type": "BUY" if is_buy else "SELL",
            "level_up": str(level_up),
            "level_down": str(level_down),
            "time": time.timestamp(),
            "price": str(level_middle),
            "status": "DEFERRED",
        }

        createdOrderId = create_order(def_ord)
        logger.info(
            f"Створення відкладенного ордеру: {def_ord["type"]}_{createdOrderId} {time}"
        )

    if len(deferred_orders) == 0 and len(active_orders) == 0:
        return

    ticks = get_ticks(SYMBOL, time, candle["next_time"])

    if ticks is None:
        # Close all active orders if no ticks are available
        del_orders = deferred_orders + active_orders
        for order in del_orders:
            delete_order(order["id"])
            logger.info(f"Видаллення ордеру {order['type']}_{order['id']} {time}")
        return

    for i, tick in enumerate(ticks.itertuples(index=False)):
        tick_bid = round_decimal(Decimal(str(tick.bid)), level="0.0000001")
        tick_log_info = f"{tick_bid} {tick.time}"

        if i == len(ticks) - 1:
            last_tick = tick_bid

        deferred_orders = get_orders({"status": "DEFERRED"})
        active_orders = get_orders({"status": "OPENED"})

        # === Check deferred orders ===
        for order in deferred_orders:
            if order["time"] == time.timestamp():
                continue
            curr_order = order.copy()
            curr_order["time"] = tick.time.timestamp()
            curr_order["price"] = tick_bid
            curr_order["level_up"] = Decimal(str(order["level_up"]))
            curr_order["level_down"] = Decimal(str(order["level_down"]))
            order_price = Decimal(str(order["price"]))

            is_buy = order["type"] == "BUY"
            is_sell = order["type"] == "SELL"

            #  OPEN ORDER
            open_condition = (is_buy and tick_bid <= order_price) or (
                is_sell and tick_bid >= order_price
            )
            if open_condition:
                curr_order["status"] = "OPENED"
                open_order_event(curr_order)
                logger.info(
                    f"Відкрито order: {order['type']}_{order["id"]}, TP: {curr_order["level_up"] if is_buy else curr_order["level_down"]}, SL: {curr_order["level_down"] if is_buy else curr_order["level_up"]}, {tick_log_info}"
                )

                continue

            #  CANCEL ORDER
            cancel_condition = (is_change_trend and is_buy and direction == "UP") or (
                is_change_trend and is_sell and direction == "DOWN"
            )
            if cancel_condition:
                cancel_order_event(curr_order)
                logger.info(
                    f"Скасовано order {order['type']}_{order["id"]} {tick_log_info}"
                )
                continue

        # === Check active orders ===
        for order in active_orders:
            curr_order = order.copy()
            curr_order["time"] = tick.time.timestamp()
            curr_order["price"] = tick_bid
            curr_order["level_up"] = Decimal(str(order["level_up"]))
            curr_order["level_down"] = Decimal(str(order["level_down"]))
            order_price = Decimal(str(order["price"]))

            is_buy = order["type"] == "BUY"
            is_sell = order["type"] == "SELL"

            #  STOP LOSS
            sl_condition = (is_buy and tick_bid < curr_order["level_down"]) or (
                is_sell and tick_bid > curr_order["level_up"]
            )
            if sl_condition:
                close_order_event(curr_order, 0)
                transaction_test(curr_order, order_price)
                logger.info(
                    f"Stop loss {order['type']}_{order["id"]}, TP: {curr_order["level_up"] if is_buy else curr_order["level_down"]}, SL: {curr_order["level_down"] if is_buy else curr_order["level_up"]}, {tick_log_info}"
                )
                logger.info(candle_info)
                continue

            #  TAKE PROFIT
            tp_condition = (is_buy and tick_bid >= curr_order["level_up"]) or (
                is_sell and tick_bid <= curr_order["level_down"]
            )
            if tp_condition:
                close_order_event(curr_order, 1)
                transaction_test(curr_order, order_price)
                logger.info(
                    f"Take profit {order['type']}_{order["id"]}, TP: {curr_order["level_up"] if is_buy else curr_order["level_down"]}, SL: {curr_order["level_down"] if is_buy else curr_order["level_up"]}, {tick_log_info}"
                )
                logger.info(candle_info)
                continue
