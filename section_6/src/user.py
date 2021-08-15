import sqlite3
from cfg import DB_PATH


class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        query = "SELECT * FROM users WHERE username = ?"
        query_results = cur.execute(query, (username,))

        result = query_results.fetchone()
        user = cls(*result) if result else None

        conn.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        query = "SELECT * FROM users WHERE id = ?"
        query_results = cur.execute(query, (_id,))

        result = query_results.fetchone()
        user = cls(*result) if result else None

        conn.close()
        return user
