from decimal import Decimal

from database.types.orders import OrderEntity
from database.repository.orders import update_order, delete_order
from database.repository.archive_orders import create_archive_order


def open_order_event(order: OrderEntity):
    update_order(order["id"], {"status": "OPENED"})
    create_archive_order(
        {
            "type": order["type"],
            "price": str(order["price"]),
            "time": order["time"],
            "profit": 0,
            "status": "OPENED",
            "id_order": order["id"],
        }
    )


def cancel_order_event(order: OrderEntity):
    create_archive_order(
        {
            "type": order["type"],
            "price": str(order["price"]),
            "time": order["time"],
            "profit": 0,
            "status": "CANCELED",
            "id_order": order["id"],
        }
    )
    delete_order(order["id"])


def close_order_event(order: OrderEntity, profit: int):
    delete_order(order["id"])
    create_archive_order(
        {
            "type": order["type"],
            "price": str(order["price"]),
            "time": order["time"],
            "profit": profit,
            "status": "CLOSED",
            "id_order": order["id"],
        }
    )
