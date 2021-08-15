from flask_restful import Resource
from cfg import DB_PATH


class ItemList(Resource):
    def get(self):
        return {"items": items}
