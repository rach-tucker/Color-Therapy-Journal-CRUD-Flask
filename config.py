import os

#just sets the base directory to our directory path (path to crud_app)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
    SECRET_KEY = os.environ.get('SECRET KEY') or 'you-will-never-guess'
    #first portion returns as none- so a file app.db is created in our directory path (creates sqlite database there)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir,'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False