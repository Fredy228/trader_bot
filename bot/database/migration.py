from database.schema.orders import order_table
from database.schema.archive_orders import archive_order_table


def migration(conn, cursor):
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS archive_orders;")
    cursor.execute(order_table)
    cursor.execute(archive_order_table)
    conn.commit()
