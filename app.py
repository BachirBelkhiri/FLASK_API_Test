# />python3 -m pip install Flask
# />python3 -m pip install Flask-RESTful #For RESTful API
# />python3 -m pip install Flask-JWT #JWT JSON WEB TOOL For Obfuscation

from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # For sqlite. You can use others like MYSQL, PostgrSQL without changing the code just this line
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# encryption key
app.secret_key = "bachir"
api = Api(app)

# This will execute the function before getting the first request (to create the db and tables)
@app.before_first_request
def create_tables():
	db.create_all()

jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)