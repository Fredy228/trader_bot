from database.types.orders import OrderEntity
from database.repository.orders import update_order, delete_order
from database.repository.archive_orders import create_archive_order


def open_order_event(order: OrderEntity):
    update_order(order.id, {"status": "OPENED"})
    del order["id"]
    del order["level_up"]
    del order["level_down"]
    order["profit"] = 0

    create_archive_order(order)


def cancel_order_event(order: OrderEntity):
    create_archive_order(
        {
            "type": order["type"],
            "price": order["price"],
            "time": order["time"],
            "profit": 0,
            "status": "CANCELED",
        }
    )
    delete_order(order["id"])
