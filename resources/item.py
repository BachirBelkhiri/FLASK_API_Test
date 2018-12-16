from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
	parser = reqparse.RequestParser()
	parser.add_argument('price', 
			type=float,
			required=True,
			help="This field cannot be left blank!"
	)
	parser.add_argument('store_id', 
			type=int,
			required=True,
			help="Every item need a store id"
	)
	@jwt_required()
	def get(self, name):
		try:
			item = ItemModel.find_by_name(name)
		except:
			return {'message': 'An error occurred while searching for the item.'}, 500
		if item:
			return item.json()
		return {'message': 'Item not found'}, 404
	
	def post(self, name):
		if ItemModel.find_by_name(name):
			return {"message": "an item with the name '{}' already exists.".format(name)}, 400 # 400 Bad Request
		data = Item.parser.parse_args()
		# item = ItemModel(name, data["price"], data["store_id"])
		item = ItemModel(name, **data)	
		try:
			item.save_to_db()
		except:
			return {'message': 'An error occurred while inserting the item.'}, 500 # 500 Internal Server Error
		return item.json(), 201 # 201 Created
	
	
	def delete(self, name):
		item = ItemModel.find_by_name(name)
		if item:
			item.delete()
			return {'message': 'Item deleted'}
		return {"message": "an item with the name '{}' doesn't exists.".format(name)}, 400 # 400 Bad Request

	def put(self, name):
		data = Item.parser.parse_args()		
		item = ItemModel.find_by_name(name)
		if item is None:
			# item = ItemModel(name, data['price'], data["store_id"])
			item = ItemModel(name, **data)
		else:
			item.price = data['price']
		item.save_to_db()
		return item.json()
	
		
class ItemList(Resource):
	def get(self):
		# return {'items': [item.json() for item in ItemModel.query.all()]}
		return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}	