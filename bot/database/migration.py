from database.orders.table import order_table


def order_migration(conn, cursor):
    cursor.execute("DROP TABLE IF EXISTS order")
    cursor.execute(order_table)
    conn.commit()
