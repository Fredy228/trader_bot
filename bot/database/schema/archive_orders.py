archive_order_table = """
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
