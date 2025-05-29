from decimal import Decimal

from services.generate_id import generate_unique_id
from services.logger import logger


deferred_orders = []


def trade_by_history_trend(level_up, level_down, direction, time):
    global deferred_orders

    is_buy = direction == "UP"
    level_middle = level_down + (level_up - level_down) * Decimal("0.5")

    def_ord = {
        "type": "BUY" if is_buy else "SELL",
        "level_up": level_up,
        "level_down": level_down,
        "time": time,
        "price": level_middle,
        "name": f"{generate_unique_id()}_{"BUY" if is_buy else "SELL"}",
    }

    deferred_orders.append(def_ord)
    logger.info(f"Створення відкладенного ордеру: {def_ord["name"]} {time}")


def get_deferred_orders():
    global deferred_orders
    return deferred_orders
