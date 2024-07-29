"""
    app: a flask restful api

"""

from flask import Flask, redirect
from web_flask.api.v1 import views
from flask_cors import CORS
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from web_flask.api.v1 import storage
from models.user import User
from flask_session import Session
import os
import redis


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY') or 'SOME RANDOM VALUE'
#CSRFProtect(app)
app.config['SESSION_COOKIE_NAME'] = 'mysession'
app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True

# I'm going to go with redis in production on ubuntu server
#app.config['SESSION_TYPE'] = 'redis'
#app.config['SESSION_PERMANENT'] = False
#app.config['SESSION_USE_SIGNER'] = True
#app.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

app.register_blueprint(views)

login = LoginManager(app)
login.login_view = 'login'
CORS(app)

#Session(app)


@login.user_loader
def load_user(id):
    return storage.get(User, id)

@app.route('/login')
def login():
    return redirect('http://127.0.0.1:5000/login')

@app.teardown_appcontext
def shutdown_session(exception=None):
    storage.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
