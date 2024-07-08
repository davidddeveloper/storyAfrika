from flask import Flask
from flask_login import LoginManager
from models.engine import storage
from web_flask.config import Config

app = Flask(__name__)
# app.config['SECRET_KEY'] = 'SOME RANDOM VALUE'
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'

from web_flask.app import routes
