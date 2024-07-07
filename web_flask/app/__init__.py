from flask import Flask
from flask_login import LoginManager
from models.engine import storage

app = Flask(__name__)
login = LoginManager(app)

from web_flask.app import routes