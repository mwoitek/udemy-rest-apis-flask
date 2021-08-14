import sqlite3
from pathlib import Path
from flask_restful import Resource
from flask_restful import reqparse
from user import User

DB_PATH = str(Path(__file__).resolve().parents[2] / "data.sqlite")


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
        args = UserRegister.parser.parse_args(strict=True)
        username = args["username"]

        user = User.find_by_username(username)
        if user:
            return {"error": f"An user with username {username} already exists"}, 400

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        sql_insert = "INSERT INTO users (username, password) VALUES (?, ?)"
        cur.execute(sql_insert, (username, args["password"]))

        conn.commit()
        conn.close()

        return {"message": "User successfully created"}, 201
