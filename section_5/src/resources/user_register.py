import sqlite3
from pathlib import Path
from flask_restful import Resource
from flask_restful import reqparse

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
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        sql_insert = "INSERT INTO users (username, password) VALUES (?, ?)"
        args = UserRegister.parser.parse_args(strict=True)
        cur.execute(sql_insert, (args["username"], args["password"]))

        conn.commit()
        conn.close()

        return {"message": "User successfully created"}, 201
