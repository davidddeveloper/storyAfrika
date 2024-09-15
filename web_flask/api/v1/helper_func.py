from flask import url_for, request, redirect, flash
from flask_login import current_user
from functools import wraps
from web_flask.api.v1.services.auth_guard import check_jwt
from web_flask.api.v1.services.auth_provider import authenticate
from models.engine import storage
from models.user import User
import os


def create_uri(dictionary=None, view=None):
    """ When the an api is returning a list of data
        This function convert the id to the uri
        pointing to the specific dictionary

        Attributes:
            - dictionary: the dictionary with an id field
            - view: the function name that handles the specific route
    """

    if dictionary is None or view is None:
        return {'Error': 'couldn\'t pass data'}

    new_dictionary = {}

    for key, val in dictionary.items():
        if key == 'id':
            if view == 'get_user':
                new_dictionary['uri'] = url_for(
                    f'views.{view}',
                    user_id=dictionary['id'],
                    _external=True
                )
            elif view == 'get_story':
                new_dictionary['uri'] = url_for(
                    f'views.{view}',
                    story_id=dictionary['id'],
                    _external=True
                )
            elif view == 'get_topic':
                new_dictionary['uri'] = url_for(
                    f'views.{view}',
                    topic_id=dictionary['id'],
                    _external=True
                )
            elif view == "get_comment_on_story":
                new_dictionary['uri'] = url_for(
                    f'views.{view}',
                    comment_id=dictionary['id'],
                    _external=True
                )
        else:
            new_dictionary[key] = val
    return new_dictionary


def check_for_valid_json(json_string, properties=[]):
    """ checks if a json is valid json
        and if the json has the neccessary properties

        Attributes:
            - json_string: the json to validate
            - properties: a list of properties to check for

    """
    if properties == []:
        return None

    if not isinstance(json_string, dict) and not isinstance(json_string, list):
        raise TypeError()

    elif isinstance(json_string, dict):
        for property in properties:
            if property not in json_string:
                return property
    elif isinstance(json_string, list) and len(json_string) < 3:
        raise ValueError()


def custom_login_required(f):
    @wraps(f)  # keep metadata about the wrapped function
    def wrapper(*args, **kwargs):
        print('current_user', current_user)
        request_url = request.url
        login_url = f'http://localhost:5000/login?next={request_url}'
        message = 'Login required to view the request page'
        if not current_user:
            flash(message)
            return redirect(login_url)
        elif not current_user.is_authenticated:
            flash(message)
            return redirect(login_url)

        return f(*args, **kwargs)

    return wrapper

def get_auth_user():
    """
        get the authenticated user

    """
    user_dict = check_jwt()
    user = authenticate(user_dict.get('email'), user_dict.get('password'))

    return user

def token_expired_error():
    pass

def validate_username(username):
    print('username ', '----------->')
    user = storage._session.query(User).where(
            User.username == username
        ).first()
    if user:
        return False
    return True

def validate_email(email):
    user = storage._session.query(User).where(
            User.email == email
        ).first()
    if user:
        return False
    return True

