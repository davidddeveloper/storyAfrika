"""
    app: a flask restful api

"""

from flask import Flask
from web_flask.api.v1 import views
from flask_cors import CORS
from flask_login import LoginManager
from web_flask.api.v1 import storage
from models.user import User


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SOME RANDOM VALUE'
app.config['SESSION_COOKIE_NAME'] = 'session'
app.config['SESSION_COOKIE_DOMAIN'] = 'localhost'
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
CORS(app, origins=['0.0.0.0'])

app.register_blueprint(views)

login = LoginManager(app)
login.login_view = 'login'


@login.user_loader
def load_user(id):
    return storage.get(User, id)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)
