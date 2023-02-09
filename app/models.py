from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
#UserMixin contains properties- is_authenticated, is_anonymous and is_active and can get_id
from flask_login import UserMixin
from app import db, login
import requests
import random

#class User inherits UserMixin properties
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    #function to set password as whatever the hash password is
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()
    
    def __repr__(self):
        return f"<User {self.id} | {self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)


@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    color_image = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # SQL Equivalent - FOREIGN KEY(user_id) REFERENCES user(id)

    def update(self,  color):
        for key, value in color.items():
            if key in {'color'}:
                setattr(self, key, value)
        db.session.commit()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.color_image = self.getImage(self.color)
        db.session.add(self)
        db.session.commit()


    #def __repr__(self):
        #return f"<Entry {self.id} | {self.title}>"
    
    #update entry on edit button
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'title', 'body'}:
                setattr(self, key, value)
        #saves to database
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def getImage(color):
        random_number = random.randint(1, 10)
        r = requests.get("https://api.unsplash.com/search/photos?query=$" + color + "&client_id=yoc9bG_ex8c11GyAK9pZt4qhGXPm6_6hkzQDiEnuXGU")
        return r.json()["results"][random_number]["urls"]["regular"]