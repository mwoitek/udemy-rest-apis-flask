from flask_jwt_extended import get_jwt_identity
from user import User

users = [
    User(1, "alice", "asdf"),
    User(2, "bob", "qwerty"),
]

username_mapping = {u.username: u for u in users}
userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and user.password == password:
        return user
    return None


def get_current_user():
    user_id = get_jwt_identity()
    return userid_mapping.get(user_id, None)
