import sqlite3
from pathlib import Path

from database.migration import migration

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "database.db"


def connect_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    return conn, cursor


def initialisation_db(conn, cursor):
    migration(conn, cursor)
    conn.close()
