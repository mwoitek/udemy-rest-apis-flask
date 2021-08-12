from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_restful import Api
from flask_restful import Resource
from security import authenticate
from security import get_current_user

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "my_secret_key"
jwt = JWTManager(app)

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


@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data.get("username", None)
    password = request_data.get("password", None)

    user = authenticate(username, password)
    if user is None:
        return jsonify({"error": "Bad username or password"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token})


@app.route("/protected")
@jwt_required()
def protected():
    user = get_current_user()
    return jsonify(
        {
            "id": user.id,
            "username": user.username,
        }
    )


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item:
            return {"error": f"An item with name {name} already exists"}, 400

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
