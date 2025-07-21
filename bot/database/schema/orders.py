order_table = """
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    time INTEGER NOT NULL,
    type TEXT CHECK(status IN ('BUY', 'SELL')) NOT NULL,
    price TEXT NOT NULL,
    level_up TEXT NOT NULL,
    level_down TEXT NOT NULL,
    status TEXT CHECK(status IN ('OPENED', 'DEFERRED')) NOT NULL
);
"""
