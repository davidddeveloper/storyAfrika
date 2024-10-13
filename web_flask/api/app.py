"""
    app: a flask restful api

"""

from flask import Flask, redirect, render_template, request, jsonify
from web_flask.api.v1 import views
from flask_cors import CORS
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from web_flask.api.v1 import storage
from models.user import User
from flask_session import Session
from web_flask.api.v1.services.jwt_handler import decode_jwt
import web_flask.api.v1.services.auth_provider as auth
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
CORS(app, origins=["http://localhost:5000", "http://192.168.212.220:5000", "http://172.20.10.3:5000", "https://special-space-waddle-v6vwgvrvj5q52wq9r-5000.app.github.dev"])

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

@app.before_request
def get_current_user():
    token = request.headers.get('Authorization')

    if token:
        jwt = token.split("Bearer ")[1]
    
        try:
            user_data = decode_jwt(jwt)
        except Exception:
            user_data = None

        if user_data and not auth.current_user:  # get the user in db
            username = user_data['username']

            user = storage._session.query(User).where(
                username == username
            ).first()
            auth.current_user = user

        if auth.current_user:
            # attached current_user to session
            auth.current_user = storage._session.merge(auth.current_user)


@app.errorhandler(404)
def handle_404(error):
    return jsonify({"Error": "not found"}), 403

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
