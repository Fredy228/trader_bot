import sqlite3

from database.connection import conn, cursor
from services.logger import logger
from database.types.orders import OrderDTO, OrderEntity


def create_order(order_data: OrderDTO) -> None:
    try:
        cursor.execute(
            """
            --sql
            INSERT INTO orders (time, type, price, level_up, level_down, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            --end-sql
        """,
            (
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
                time=row[1],
                type=row[2],
                price=row[3],
                level_up=row[4],
                level_down=row[5],
                status=row[6],
            )
        return None
    except sqlite3.Error as e:
        logger.error(f"An error occurred while getting order: {e}")
        return None


def get_orders(filters: dict = None) -> list[OrderEntity]:
    try:
        query = "SELECT * FROM orders"
        values = []

        if filters:
            conditions = []
            for key, value in filters.items():
                conditions.append(f"{key} = ?")
                values.append(value)
            query += " WHERE " + " AND ".join(conditions)

        cursor.execute(query, values)
        rows = cursor.fetchall()

        return [
            OrderEntity(
                id=row[0],
                time=row[1],
                type=row[2],
                price=row[3],
                level_up=row[4],
                level_down=row[5],
                status=row[6],
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


def delete_order(order_id: int) -> None:
    try:
        cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred while deleting order: {e}")
