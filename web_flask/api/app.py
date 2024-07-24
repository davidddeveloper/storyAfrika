"""
    app: a flask restful api

"""

from flask import Flask
from web_flask.api.v1 import views
from flask_cors import CORS
from flask_login import LoginManager
from web_flask.api.v1 import storage
from models.user import User
from flask_session import Session
import os
import redis


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'SOME RANDOM VALUE'
#app.config['SESSION_COOKIE_NAME'] = 'mysession'
#app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'
#app.config['SESSION_COOKIE_SAMESITE'] = 'None'
#app.config['SESSION_COOKIE_SECURE'] = True

# I'm going to go with redis in production on ubuntu server
#app.config['SESSION_TYPE'] = 'redis'
#app.config['SESSION_PERMANENT'] = False
#app.config['SESSION_USE_SIGNER'] = True
#app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')
#Session(app)

app.register_blueprint(views)

login = LoginManager(app)
login.login_view = 'login'
CORS(app, resources={r"/*": {"origins": "*"}})


@login.user_loader
def load_user(id):
    return storage.get(User, id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
