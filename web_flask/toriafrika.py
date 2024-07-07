from web_flask.app import app, login, storage
from models.user import User


@login.user_loader
def load_user(id):
    return storage.get(User, id)
