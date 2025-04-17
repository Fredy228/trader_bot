import os
import sqlite3

from database.migration import migration

appdata_path = os.environ.get("AppData")

db_dir = os.path.join(appdata_path, "TradingBot")
db_path = os.path.join(db_dir, "database.db")

os.makedirs(db_dir, exist_ok=True)


def connect_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    return conn, cursor


def initialisation_db():
    conn, cursor = connect_db()
    migration(conn, cursor)
    conn.close()
