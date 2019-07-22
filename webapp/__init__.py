from flask import Flask
#from flask_sqlalchemy import SQLAlchemy
from webapp.config import Config

app = Flask(__name__)
app.config.from_object(Config)

#db = SQLAlchemy(app)

from webapp.main.routes import main
from webapp.errors.handlers import errors
app.register_blueprint(main)
app.register_blueprint(errors)
