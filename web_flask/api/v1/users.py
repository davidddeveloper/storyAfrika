"""
    users: rest api for creating users

"""

from flask import request, jsonify, abort, url_for
from flask_login import current_user, login_required
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from web_flask.api.v1.helper_func import custom_login_required
from models.user import User
from models.follower import Follower
from web_flask.api.v1 import storage


@views.route(
    '/users/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@login_required
def users():
    """ Get all users or creates a user """

    if request.method == 'POST':
        # checks for valid json
        try:
            user_json = request.get_json()
            check_for_valid_json(user_json, ['username', 'email', 'password'])

        except Exception:
            return jsonify({"Error": 'not a valid json'}), 400

        else:
            if isinstance(user_json, dict):
                user = User(
                        username=user_json['username'],
                        email=user_json['email'],
                        password=user_json['password']
                    )
            elif isinstance(user_json, list):
                user = User(
                    username=user_json[0],
                    email=user_json[1],
                    password=user_json[2]
                )
            storage.new(user)
            storage.save()
            print(user)
            return jsonify(user.to_dict()), 201

    users = storage.all(User)

    return jsonify(
        [create_uri(user.to_dict(), 'get_user') for user in users.values()]
    ), 200


@views.route(
    '/users/<int:n>/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@login_required
def limit_users(n=None):
    """ Limits the number of users to get

        Attributes:
            - n: a number representing the amount of users to get

    """

    if n is None:
        abort(404)

    users = storage.all(User)
    limited_users = {}
    counter = 0

    for key, val in users.items():
        if counter == n:
            break

        limited_users[key] = val
        counter += 1

    return jsonify(
        [
            create_uri(user.to_dict(), 'get_user')
            for user in limited_users.values()
        ]
    ), 200


@views.route(
    '/users/<string:user_id>/',
    methods=['GET', 'PUT'],
    strict_slashes=False
)
@login_required
def get_user(user_id=None):
    """ Gets a specific user or update an existing one """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if request.method == 'PUT':
        try:
            user_json = request.get_json()
            check_for_valid_json(user_json, ['username', 'email', 'password'])

        except Exception:
            return jsonify({"Error": 'not a valid json'}), 400

        else:
            for key, val in user_json.items():
                if key not in ['id', 'created_at', 'updated_at']:
                    setattr(user, key, val)

            storage.save()

    return jsonify(user.to_dict()), 200


@views.route(
    '/users/<string:user_id>/stories/',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def get_story_of_user(user_id=None):
    user = storage.get(User, user_id)

    if user is None:
        abort(404)
    stories = [story.to_dict() for story in user.stories]
    return jsonify([create_uri(story, 'get_story') for story in stories]), 200


@views.route(
    '/users/<string:user_id>/stories/<int:n>',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def limit_story_of_user(user_id=None, n=None):
    """ Limits the number of stories to get for a particular user

        Attributes:
            - user_id: the id of the user
            - n: a number representing the amount of stories to get

    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    stories = [story for story in user.stories]

    limited_stories = {}
    counter = 0
    for story_obj in stories:
        if counter == n:
            break

        limited_stories = [story_obj]
        counter += 1

    return jsonify(
        [
            create_uri(story.to_dict(), 'get_user')
            for story in limited_stories
        ]
    ), 200


@views.route(
    '/users/<string:user_id>/',
    methods=['DELETE'],
    strict_slashes=False
)
@login_required
def delete_user(user_id=None):
    """ Deletes a user """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({"Deleted": user.to_dict()})


@views.route(
    '/users/<string:user_id>/followers',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def get_user_followers(user_id=None):
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    followers = storage._session.scalars(user.followers.select()).all()

    return jsonify([
        follower.to_dict() for follower in followers
    ])


@views.route(
    '/users/<string:user_id>/following',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def get_user_following(user_id=None):
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    followings = user.following

    return jsonify([
        following.to_dict() for following in followings
    ])


@views.route(
    '/users/<string:user_id>/follow',
    methods=['POST'],
    strict_slashes=False
)
@login_required
def follow_or_unfollow_user(user_id=None):
    """ Follow or unfollow a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if current_user.is_following(user):
        current_user.following.remove(user)
    else:
        current_user.following.add(user)

    storage.save()

    return jsonify({}), 201
