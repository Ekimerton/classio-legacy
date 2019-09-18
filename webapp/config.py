import os


class Config:
    # App
    try:
        SECRET_KEY = os.environ['SECRET_KEY']
        DEBUG = False
    except:
        SECRET_KEY = 'test'
        DEBUG = True
    # Database
    #SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    #SQLALCHEMY_TRACK_MODIFICATIONS = os.environ['SQLALCHEMY_TRACK_MODIFICATIONS']
