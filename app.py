# />python3 -m pip install Flask
# />python3 -m pip install Flask-RESTful #For RESTful API
# />python3 -m pip install Flask-JWT #JWT JSON WEB TOOL For Obfuscation
import os
from flask import Flask
from flask_restful import Resource, Api
from flask_jwt import JWT
from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList


app = Flask(__name__)
# For sqlite. You can use others like MYSQL, PostgrSQL without changing the code just this line
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' 
# After deploying it to Heroku we need to use the postgres to not loose the data.
# So we use os to get the environement variable that matches the postgres database URL or the sqlite db url for backup
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','sqlite:///data.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# encryption key
app.secret_key = "bachir"
api = Api(app)


jwt = JWT(app, authenticate, identity)

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(StoreList, '/stores')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	app.run(port=5000, debug=True)