from app.data import db
from app.data import CRUDMixin

class Base(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

class User(Base,CRUDMixin):
    __tablename__='users'
    telegramid = db.Column(db.String(128), nullable=False)
   

    def __init__(self,telegramid):
	self.telegramid = telegramid

    def get_id(self):
	return self.id

    def serialize(self):
	return {'telegramid':self.telegramid}
    def serialize_all(self):
	return {'telegramid':self.telegramid}
    def __repr__(self):
	return '<user telegramid=%r>' % (self.telegramid)
      
class Log(Base,CRUDMixin):
	__tablename__ = 'logs'
	textlog = db.Column(db.String(600), nullable=False)
	username= db.Column(db.String(128), nullable=False)
	def __init__(self,textlog,username):
		self.textlog = textlog
		self.username = username
	def get_log(self):
		return self.textlog
	def serialize(self):
		return {'textlog':self.textlog, 'username': self.username}
    	def __repr__(self):
		return '<log textlog=%r username=%r>' % (self.textlog, self.username)

