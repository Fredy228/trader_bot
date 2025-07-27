from database.schema.orders import migrate_order_table
from database.schema.archive_orders import migrate_archive_order_table


def migration(conn, cursor):
    migrate_order_table(conn, cursor)
    migrate_archive_order_table(conn, cursor)
