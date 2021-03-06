import sqlite3
from cfg import DB_PATH

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Users
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        username TEXT,
        password TEXT
    )
    """
)

# Items
cur.execute("CREATE TABLE IF NOT EXISTS items (name TEXT, price REAL)")

conn.commit()
conn.close()
