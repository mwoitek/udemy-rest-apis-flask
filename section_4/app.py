from flask import Flask
from flask import request
from flask_restful import Api
from flask_restful import Resource

app = Flask(__name__)
api = Api(app)

items = [
    {
        "name": "Keyboard",
        "price": 200,
    },
    {
        "name": "Mouse",
        "price": 30.5,
    },
    {
        "name": "Laptop",
        "price": 3000,
    },
]


class Item(Resource):
    def get(self, name):
        for item in items:
            if item["name"] == name:
                return item
        return {"item": None}, 404

    def post(self, name):
        request_data = request.get_json()
        item = {
            "name": name,
            "price": request_data["price"],
        }
        items.append(item)
        return item, 201


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


if __name__ == "__main__":
    app.run(port=5000)
