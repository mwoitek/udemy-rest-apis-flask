from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_restful import Api
from flask_restful import Resource
from flask_restful import reqparse
from security import authenticate
from security import get_current_user

app = Flask(__name__)

# Setup Flask-JWT-Extended
# TODO Get the secret key from an environment variable
app.config["JWT_SECRET_KEY"] = "my_secret_key"
jwt = JWTManager(app)


# TODO Add more callbacks like this so that every authentication-related error
# is handled
@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"error": "Token has expired"}), 401


api = Api(app)

items = [
    {
        "name": "Keyboard",
        "price": 200.0,
    },
    {
        "name": "Mouse",
        "price": 30.5,
    },
    {
        "name": "Laptop",
        "price": 3000.0,
    },
]


@app.route("/login", methods=["POST"])
def login():
    request_data = request.get_json()
    username = request_data.get("username", None)
    password = request_data.get("password", None)

    user = authenticate(username, password)
    if user is None:
        return jsonify({"error": "Unable to login"}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token})


# This route is not really necessary. Its only purpose is to show how we can
# get the identity of an authenticated user.
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
    # Validate request data
    parser = reqparse.RequestParser()
    parser.add_argument(
        "price",
        type=float,
        required=True,
        help="Item price has to be specified",
    )

    @staticmethod
    def find_item_by_name(name):
        return next(filter(lambda x: x["name"] == name, items), None)

    def get(self, name):
        item = Item.find_item_by_name(name)
        if item:
            return {"item": item}
        return {"error": f"Item named {name} does not exist"}, 404

    @jwt_required()
    def post(self, name):
        item = Item.find_item_by_name(name)
        if item:
            return {"error": f"An item named {name} already exists"}, 400

        args = Item.parser.parse_args(strict=True)
        item = {
            "name": name,
            "price": args["price"],
        }
        items.append(item)
        return item, 201

    @jwt_required()
    def delete(self, name):
        item = Item.find_item_by_name(name)
        if item is None:
            return {"error": f"Item named {name} does not exist"}, 404

        item_idx = items.index(item)
        items.pop(item_idx)
        return {
            "message": "Item successfully removed",
            "item": item,
        }

    @jwt_required()
    def put(self, name):
        args = Item.parser.parse_args(strict=True)

        item = Item.find_item_by_name(name)
        if item is None:
            # Create item
            item = {
                "name": name,
                "price": args["price"],
            }
            items.append(item)
            return item, 201

        # Update item
        item.update(args)
        return {
            "message": "Item successfully updated",
            "item": item,
        }


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


if __name__ == "__main__":
    app.run(port=5000)
