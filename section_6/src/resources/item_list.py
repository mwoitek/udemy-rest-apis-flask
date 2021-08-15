import sqlite3
from flask_restful import Resource
from cfg import DB_PATH


class ItemList(Resource):
    def get(self):
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            query_results = cur.execute("SELECT * FROM items").fetchall()
            conn.close()
        except Exception:
            return {"message": "Unable to get items"}, 500

        items = [{"name": name, "price": price} for name, price in query_results]
        return {"items": items}
