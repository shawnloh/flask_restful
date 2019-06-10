from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_claims

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True,
                        help="Price is required")
    parser.add_argument('store_id', type=int, required=True,
                        help="Store id is required")

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {
            'message': 'Item not found'
        }, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {
                'message': 'Item with name {} already exist'.format(name)
            }, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {
                'message': 'An error occurred inserting the item.'
            }, 500

        return item.json(), 201

    @jwt_required
    def delete(self, name):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {
                'message': 'Admin privilege required.'
            }, 401

        item = ItemModel.find_by_name(name)

        if item:
            item.delete()

        return {
            'message': '{} deleted'.format(name)
        }

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {
            'items': [item.json() for item in ItemModel.find_all()]
        }
        # return {
        #     'items': list(map(lambda x: x.json(), ItemModel.query.all()))
        # }
