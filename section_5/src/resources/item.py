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
        help="Item price has to be specified",
    )

    @staticmethod
    def find_by_name(name):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        query = "SELECT * FROM items WHERE name = ?"
        query_results = cur.execute(query, (name,))
        result = query_results.fetchone()

        conn.close()
        return result

    def get(self, name):
        result = Item.find_by_name(name)
        if result:
            item = {
                "name": name,
                "price": result[1],
            }
            return {"item": item}
        return {"error": f"Item named {name} does not exist"}, 404

    @jwt_required()
    def post(self, name):
        item = Item.find_by_name(name)
        if item:
            return {"error": f"An item named {name} already exists"}, 400

        args = Item.parser.parse_args(strict=True)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        sql_insert = "INSERT INTO items (name, price) VALUES (?, ?)"
        cur.execute(sql_insert, (name, args["price"]))

        conn.commit()
        conn.close()

        return {"message": "Item successfully created"}, 201

    # @jwt_required()
    # def delete(self, name):
    #     item = Item.find_item_by_name(name)
    #     if item is None:
    #         return {"error": f"Item named {name} does not exist"}, 404

    #     item_idx = items.index(item)
    #     items.pop(item_idx)
    #     return {
    #         "message": "Item successfully removed",
    #         "item": item,
    #     }

    # @jwt_required()
    # def put(self, name):
    #     args = Item.parser.parse_args(strict=True)

    #     item = Item.find_item_by_name(name)
    #     if item is None:
    #         # Create item
    #         item = {
    #             "name": name,
    #             "price": args["price"],
    #         }
    #         items.append(item)
    #         return item, 201

    #     # Update item
    #     item.update(args)
    #     return {
    #         "message": "Item successfully updated",
    #         "item": item,
    #     }
