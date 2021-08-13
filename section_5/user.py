import sqlite3
from flask_restful import Resource
from flask_restful import reqparse

DB_PATH = "data.sqlite"


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


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        "username",
        type=str,
        required=True,
        help="Unable to create an user with no username",
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,
        help="Unable to create an user with no password",
    )

    def post(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        sql_insert = "INSERT INTO users (username, password) VALUES (?, ?)"
        args = UserRegister.parser.parse_args(strict=True)
        cur.execute(sql_insert, (args["username"], args["password"]))

        conn.commit()
        conn.close()

        return {"message": "User successfully created"}, 201
