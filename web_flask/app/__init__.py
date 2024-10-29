from flask import Flask
from humanize_number.humanize_flask import init_app
from flask_login import LoginManager
from models.engine import storage
from web_flask.config import Config
from flask_moment import Moment
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_cors import CORS

app = Flask(__name__)
init_app(app)
# app.config['SECRET_KEY'] = 'SOME RANDOM VALUE'
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)
#CSRFProtect(app)
#Session(app)

from web_flask.app import routes
