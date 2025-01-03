# *1 The decorated function is expected to return the same types of value than a typical flask view function, except the body part may be an object or a list of objects to serialize with the schema, rather than a string.
import uuid
from flask import request
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt
from flask_smorest import abort, Blueprint
# from db import items, stores
from sqlalchemy.exc import SQLAlchemyError
from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint('items', __name__, description="Operations on items")

@blp.route('/item/<string:item_id>')
class Item(MethodView):
    @blp.response(200, ItemSchema) # *1 What should be returned ?
    def get(self, item_id):
        item = ItemModel.query.get_or_404(id=item_id)
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        # item_data = request.get_json()
        item = ItemModel.query.get(id=item_id)
        if item:
            item.price = item_data['price']
            item.name = item_data['name']
        else:
            item = ItemModel(id=item_id, **item_data)
        db.session.add(item)
        db.session.commit()

        return item

    @jwt_required()
    def delete(self, item_id):
        jwt = get_jwt()
        if not jwt.get("is_admin"):
            abort(401, message="Admin privilege required.")

        item = ItemModel.query.get_or_404(id=item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted"}

@blp.route('/item')
class ItemList(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    # Without the  validation schema
    # def post(self):
    #     item_data = request.get_json()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        # for item in items.values():
        #     if (
        #             item_data["name"] == item["name"]
        #             and item_data["store_id"] == item["store_id"]
        #     ):
        #         abort(400, message="Item already exists")
        #
        # if item_data["store_id"] not in stores:
        #     abort(404, message="Store not found")
        # item_id = uuid.uuid4().hex
        # item = {**item_data, "item_id": item_id}
        # items[item_id] = item
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Something went wrong")

        return item
