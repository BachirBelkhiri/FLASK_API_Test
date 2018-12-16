from db import db

class StoreModel(db.Model):
	# specify the db table name
	__tablename__ = 'stores'
    
	# specify the table columns
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(80))

	items = db.relationship('ItemModel', lazy='dynamic')

	def __init__(self, name):
		self.name = name

	def json(self):
		return {'name': self.name, 'items': [item.json() for item in self.items.all()]}

	@classmethod
	def find_by_name(cls, name):
		return cls.query.filter_by(name=name).first()

	def save_to_db(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()