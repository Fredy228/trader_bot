import os
import sqlite3

appdata_path = os.environ.get("AppData")

db_dir = os.path.join(appdata_path, "TradingBot")
db_path = os.path.join(db_dir, "database.db")

os.makedirs(db_dir, exist_ok=True)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()
