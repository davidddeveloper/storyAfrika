from flask import Blueprint, redirect
from models.engine import storage

views = Blueprint('views', __name__, url_prefix='/api/v1')


from web_flask.api.v1.comments import *
from web_flask.api.v1.stories import *
from web_flask.api.v1.topics import *
from web_flask.api.v1.users import *
from web_flask.api.v1.auth import *
from web_flask.api.v1.search import *
from web_flask.api.v1.register import *
from web_flask.api.v1.file_uploads import *
from web_flask.api.v1.assistive_writing import *