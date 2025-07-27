import sqlite3
from pathlib import Path

from database.migration import migration

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "database.db"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

migration(conn, cursor)
