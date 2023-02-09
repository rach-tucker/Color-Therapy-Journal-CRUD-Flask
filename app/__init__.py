#the flask run command runs this exact file(it is a python package)

#imports the Flask class(becomes main object)
from flask import Flask

#import SQLAlchemy and Migrate classes:
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager




#this imports the Config class created in config.py (this just helps keep things organized)
from config import Config

#create an instance of the Flask Class called app:
app = Flask(__name__)

#from_object method takes in the class Config and takes all uppercase attributes and sets those as key-value pairs(SECRET_KEY = value)
app.config.from_object(Config)

#create an instance of SQLAlchemy for our database: (connecting app and database)
db = SQLAlchemy(app)

#create an instance of Migrate for our migration engine:(takes in the app and database(SQLAlchemy)) **flask db init will create a migrations folder**
# to add tables to migrations- flask db migrate -m "message"
#to see tables in SQLite- ctrl + shift + p - search SQLite
#may need to use - flask db upgrade - to see new tables
migrate = Migrate(app, db)

#create instanceof LoginManager to get up login functionality
login = LoginManager(app)
#this redirects unauthorized users
login.login_view = 'login'
login.login_message='You must be logged in to perform this action'
login.login_message_category= 'danger'

#should always be at the bottom(imports all routes and models)
from . import routes, models