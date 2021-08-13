import sqlite3

DB_PATH = "data.sqlite"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        username TEXT,
        password TEXT
    )
    """
)

conn.commit()
conn.close()
