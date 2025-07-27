archive_order_table_create = """
--sql
CREATE TABLE IF NOT EXISTS archive_orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time INTEGER NOT NULL,
    type TEXT CHECK(status IN ('BUY', 'SELL')) NOT NULL,
    price TEXT NOT NULL,
    status TEXT CHECK(status IN ('OPENED', 'CLOSED', 'CANCELED')) NOT NULL,
    profit INTEGER
);
"""

archive_order_table_drop = """
--sql
DROP TABLE IF EXISTS archive_orders;
"""

archive_order_table_id_idx = """
--sql
CREATE INDEX IF NOT EXISTS idx_order_id ON archive_orders (id);
"""

archive_order_table_time_idx = """
--sql
CREATE INDEX IF NOT EXISTS idx_order_time ON archive_orders (time);
"""

archive_order_table_status_idx = """
--sql
CREATE INDEX IF NOT EXISTS idx_order_status ON archive_orders (status);
"""


def migrate_archive_order_table(conn, cursor):
    cursor.execute(archive_order_table_drop)
    cursor.execute(archive_order_table_create)
    cursor.execute(archive_order_table_id_idx)
    cursor.execute(archive_order_table_time_idx)
    cursor.execute(archive_order_table_status_idx)
    conn.commit()
