order_table_create = """
--sql
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    time INTEGER NOT NULL,
    type TEXT CHECK(status IN ('BUY', 'SELL')) NOT NULL,
    price TEXT NOT NULL,
    level_up TEXT NOT NULL,
    level_down TEXT NOT NULL,
    status TEXT CHECK(status IN ('OPENED', 'DEFERRED')) NOT NULL
);
"""

order_table_drop = """
--sql
DROP TABLE IF EXISTS orders;
"""

order_table_id_idx = """
--sql
CREATE INDEX IF NOT EXISTS idx_order_id ON orders (id);
"""

order_table_time_idx = """
--sql
CREATE INDEX IF NOT EXISTS idx_order_time ON orders (time);
"""

order_table_status_idx = """
--sql
CREATE INDEX IF NOT EXISTS idx_order_status ON orders (status);
"""


def migrate_order_table(conn, cursor):
    cursor.execute(order_table_drop)
    cursor.execute(order_table_create)
    cursor.execute(order_table_id_idx)
    cursor.execute(order_table_time_idx)
    cursor.execute(order_table_status_idx)
    conn.commit()
