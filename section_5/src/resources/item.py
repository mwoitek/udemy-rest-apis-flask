import sqlite3
from pathlib import Path
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from flask_restful import reqparse

DB_PATH = str(Path(__file__).resolve().parents[2] / "data.sqlite")


class Item(Resource):
    # Validate request data
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="It is required to specify a number as the item price",
    )

    @staticmethod
    def find_by_name(name):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            query = "SELECT * FROM items WHERE name = ?"
            query_results = cur.execute(query, (name,))
            result = query_results.fetchone()

            conn.close()
            return result
        except Exception as e:
            raise e

    def get(self, name):
        try:
            result = Item.find_by_name(name)
        except Exception:
            return {"message": "Unable to get item"}, 500

        if result:
            item = {
                "name": name,
                "price": result[1],
            }
            return {"item": item}
        return {"message": f"Item named {name} does not exist"}, 404

    @staticmethod
    def insert(name, price):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            sql_insert = "INSERT INTO items (name, price) VALUES (?, ?)"
            cur.execute(sql_insert, (name, price))

            conn.commit()
            conn.close()
        except Exception as e:
            raise e

    @jwt_required()
    def post(self, name):
        try:
            item = Item.find_by_name(name)
        except Exception:
            return {"message": "Unable to check if item already exists"}, 500

        if item:
            return {"message": f"An item named {name} already exists"}, 400

        args = Item.parser.parse_args(strict=True)

        try:
            Item.insert(name, args["price"])
            return {"message": "Item successfully created"}, 201
        except Exception:
            return {"message": "Unable to insert item into database"}, 500

    @jwt_required()
    def delete(self, name):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            sql_delete = "DELETE FROM items WHERE name = ?"
            cur.execute(sql_delete, (name,))
            deleted = cur.rowcount == 1

            conn.commit()
            conn.close()
        except Exception:
            return {"message": "Unable to delete item"}, 500

        if deleted:
            return {"message": "Item successfully deleted"}
        return {"message": f"Item named {name} does not exist"}, 404

    @jwt_required()
    def put(self, name):
        args = Item.parser.parse_args(strict=True)

        try:
            item = Item.find_by_name(name)
        except Exception:
            return {"message": "Unable to check if item already exists"}, 500

        # Create item
        if item is None:
            try:
                Item.insert(name, args["price"])
                return {"message": "Item successfully created"}, 201
            except Exception:
                return {"message": "Unable to insert item into database"}, 500

        # Update item
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()

            sql_update = "UPDATE items SET price = ? WHERE name = ?"
            cur.execute(sql_update, (args["price"], name))

            conn.commit()
            conn.close()

            return {"message": "Item successfully updated"}
        except Exception:
            return {"message": "Unable to update item"}, 500
