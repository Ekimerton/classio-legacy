import os

class Config:
    # App
    SECRET_KEY = os.environ['SECRET_KEY']

    # Database
    #SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    #SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
