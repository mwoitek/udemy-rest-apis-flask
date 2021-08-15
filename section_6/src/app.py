from flask import Flask
from flask import jsonify
from flask import request
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_restful import Api

from item import Item
from item_list import ItemList
from security import authenticate
from security import get_current_user
from user_register import UserRegister

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


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")


if __name__ == "__main__":
    app.run(port=5000)
