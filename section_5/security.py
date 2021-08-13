from flask_jwt_extended import get_jwt_identity
from user import User


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user
    return None


def get_current_user():
    user_id = get_jwt_identity()
    return User.find_by_id(user_id)
