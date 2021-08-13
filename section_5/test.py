import sqlite3

conn = sqlite3.connect("data.sqlite")
cur = conn.cursor()

# Make sure we always start fresh
cur.execute("DROP TABLE IF EXISTS users")

cur.execute(
    "CREATE TABLE users (id INTEGER, username TEXT, password TEXT)",
)

# Insert a single user
user = (1, "alice", "asdf123")
cur.execute(
    "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
    user,
)

# Insert several users
users = [
    (2, "bob", "qwerty987"),
    (3, "carol", "abc1234"),
]
cur.executemany(
    "INSERT INTO users (id, username, password) VALUES (?, ?, ?)",
    users,
)

query_results = cur.execute("SELECT * FROM users")
for result in query_results:
    print(result)

conn.commit()
conn.close()
