from app import app
from db import db

db.init_app(app)

# This will execute the function before getting the first request (to create the db and tables)
@app.before_first_request
def create_tables():
	db.create_all()
