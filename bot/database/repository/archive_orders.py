import sqlite3

from database.connection import conn, cursor
from services.logger import logger
from database.types.orders_archive import OrderArchiveDTO, OrderArchiveEntity


def create_archive_order(order_data: OrderArchiveDTO) -> None:
    try:
        cursor.execute(
            """
            --sql
            INSERT INTO orders (name, time, type, price, status, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            --end-sql
        """,
            (
                order_data["name"],
                order_data["time"],
                order_data["type"],
                order_data["price"],
                order_data["status"],
                order_data["profit"],
            ),
        )
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred while creating order: {e}")


def get_archive_order_by_id(order_id: int) -> OrderArchiveEntity | None:
    try:
        cursor.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if row:
            return OrderArchiveEntity(
                id=row[0],
                name=row[1],
                time=row[2],
                type=row[3],
                price=row[4],
                status=row[5],
                profit=row[6],
            )
        return None
    except sqlite3.Error as e:
        logger.error(f"An error occurred while getting order: {e}")
        return None


def get_archive_orders() -> list[OrderArchiveEntity]:
    try:
        cursor.execute("SELECT * FROM orders")
        rows = cursor.fetchall()
        return [
            OrderArchiveEntity(
                id=row[0],
                name=row[1],
                time=row[2],
                type=row[3],
                price=row[4],
                status=row[5],
                profit=row[6],
            )
            for row in rows
        ]
    except sqlite3.Error as e:
        logger.error(f"An error occurred while getting orders: {e}")
        return []


def update_archive_order(order_id: int, order_data: OrderArchiveDTO) -> None:
    try:
        set_clause = ", ".join([f"{key} = ?" for key in order_data])
        values = list(order_data.values())
        values.append(order_id)

        query = f"UPDATE orders SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred while updating order: {e}")
