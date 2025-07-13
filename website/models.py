from . import db
from sqlalchemy.orm import validates 
from flask_login import UserMixin



class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    contacts = db.relationship('Contact', backref='user', lazy=True)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("Invalid email address")
        elif User.query.filter_by(email=address).first():
            raise ValueError("Email already exsists")
        return address
    
    def set_password(self, password):
        self.password = password

    def cheack_password(self, password):
        return self.password == password    

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # @validates('email')
    # def validate_email(self, address):
    #     if '@' not in address:
    #         raise ValueError("Invalid email address")
    #     return address