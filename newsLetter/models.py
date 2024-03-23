from . import db
from flask_login import UserMixin

class Subscribers(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    email = db.Column(db.String(40), unique = True, nullable = False)

    def __repr__(self):
        return f"{self.id}, name: {self.name}, email: {self.email}, verification status: {self.verified}"
    
class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(40), unique = True, nullable = False)
    password = db.Column(db.String(60), nullable = False)





