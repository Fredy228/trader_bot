import sqlite3

from database.connection import conn, cursor
from services.logger import logger
from database.types.orders import OrderDTO, OrderEntity


def create_order(order_data: OrderDTO) -> None:
    try:
        cursor.execute(
            """
            --sql
            INSERT INTO orders (name, time, type, price, level_up, level_down, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            --end-sql
        """,
            (
                order_data["name"],
                order_data["time"],
                order_data["type"],
                order_data["price"],
                order_data["level_up"],
                order_data["level_down"],
                order_data["status"],
            ),
        )
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred while creating order: {e}")


def get_order_by_id(order_id: int) -> OrderEntity | None:
    try:
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if row:
            return OrderEntity(
                id=row[0],
                name=row[1],
                time=row[2],
                type=row[3],
                price=row[4],
                level_up=row[5],
                level_down=row[6],
                status=row[7],
            )
        return None
    except sqlite3.Error as e:
        logger.error(f"An error occurred while getting order: {e}")
        return None


def get_orders() -> list[OrderEntity]:
    try:
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        return [
            OrderEntity(
                id=row[0],
                name=row[1],
                time=row[2],
                type=row[3],
                price=row[4],
                level_up=row[5],
                level_down=row[6],
                status=row[7],
            )
            for row in rows
        ]
    except sqlite3.Error as e:
        logger.error(f"An error occurred while getting orders: {e}")
        return []


def update_order(order_id: int, order_data: OrderDTO) -> None:
    try:
        set_clause = ", ".join([f"{key} = ?" for key in order_data])
        values = list(order_data.values())
        values.append(order_id)

        query = f"UPDATE orders SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred while updating order: {e}")
