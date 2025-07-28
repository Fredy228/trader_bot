import sqlite3

from database.connection import conn, cursor
from services.logger import logger
from database.types.orders_archive import OrderArchiveDTO, OrderArchiveEntity


def create_archive_order(order_data: OrderArchiveDTO) -> None:
    try:
        cursor.execute(
            """
            --sql
            INSERT INTO archive_orders (time, type, price, status, profit, id_order)
            VALUES (?, ?, ?, ?, ?, ?)
            --end-sql
        """,
            (
                order_data["time"],
                order_data["type"],
                order_data["price"],
                order_data["status"],
                order_data["profit"],
                order_data["id_order"],
            ),
        )
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred while creating archive order: {e}")


def get_archive_order_by_id(order_id: int) -> OrderArchiveEntity | None:
    try:
        cursor.execute("SELECT * FROM archive_orders WHERE id = ?", (order_id,))
        row = cursor.fetchone()
        if row:
            return OrderArchiveEntity(
                id=row[0],
                time=row[1],
                type=row[2],
                price=row[3],
                status=row[4],
                profit=row[5],
                id_order=row[6],
            )
        return None
    except sqlite3.Error as e:
        logger.error(f"An error occurred while getting archive order: {e}")
        return None


def get_archive_orders() -> list[OrderArchiveEntity]:
    try:
        cursor.execute("SELECT * FROM archive_orders")
        rows = cursor.fetchall()
        return [
            OrderArchiveEntity(
                id=row[0],
                time=row[1],
                type=row[2],
                price=row[3],
                status=row[4],
                profit=row[5],
                id_order=row[6],
            )
            for row in rows
        ]
    except sqlite3.Error as e:
        logger.error(f"An error occurred while getting archive orders: {e}")
        return []


def update_archive_order(order_id: int, order_data: OrderArchiveDTO) -> None:
    try:
        set_clause = ", ".join([f"{key} = ?" for key in order_data])
        values = list(order_data.values())
        values.append(order_id)

        query = f"UPDATE archive_orders SET {set_clause} WHERE id = ?"
        cursor.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        logger.error(f"An error occurred while updating archive order: {e}")
