"""
    users: rest api for creating users

"""

from flask import request, jsonify, abort
from flask_login import current_user
from models.story import Story
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri
from web_flask.api.v1.helper_func import check_for_valid_json
from web_flask.api.v1.helper_func import validate_username
from web_flask.api.v1.helper_func import validate_email
from models.user import User
from web_flask.api.v1 import storage
from web_flask.api.v1.services.data_service import get_story_data
from web_flask.api.v1.services.data_service import get_user_data
from web_flask.api.v1.services.auth_guard import auth_guard
import web_flask.api.v1.services.auth_provider as auth


@views.route(
    '/users/',
    strict_slashes=False,
    methods=['GET']
)
@auth_guard
def users():
    """ Get all users """
    users = storage.all(User)

    return jsonify(
        [create_uri(get_user_data(user), 'get_user') for user in users.values()]
    ), 200


@views.route(
    '/users/<int:n>/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@auth_guard
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
            create_uri(get_user_data(user), 'get_user')
            for user in limited_users.values()
        ]
    ), 200


@views.route(
    '/users/<string:user_id>/',
    methods=['GET', 'PUT'],
    strict_slashes=False
)
@auth_guard
def get_user(user_id=None):
    """ Gets a specific user or update an existing one """
    user = storage.get(User, user_id)

    if not auth.authorize(user):
        return jsonify({"Error": "Permission denied!"}), 403

    if user is None:
        abort(404)

    return jsonify(get_user_data(user)), 200


@views.route(
    '/users/me/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_current_user():
    """ Gets a specific user or update an existing one """

    if not auth.authorize(auth.current_user):
        return jsonify({"Error": "Permission denied!"}), 403

    return jsonify(get_user_data(auth.current_user)), 200


@views.route(
    '/users/',
    methods=['PUT'],
    strict_slashes=False
)
@auth_guard
def update_user():
    if not auth.current_user:
        abort(404)
    
    if not auth.authorize(auth.current_user):
        return jsonify({"Error": "Permission denied!"}), 403

    try:
        user_json = request.get_json()
        check_for_valid_json(user_json, ['username', 'email', 'password'])

    except Exception:
        return jsonify({"Error": 'not a valid json'}), 400

    else:
        for key, val in user_json.items():
            if key not in ['id', 'created_at', 'updated_at', 'role']:
                setattr(auth.current_user, key, val)

        storage.save()
    
    return jsonify(get_user_data(auth.current_user)), 204

@views.route(
    '/users/stories/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_story_of_user():
    if auth.current_user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    stories = []

    for story in auth.current_user.stories:
        stories.append(create_uri(get_story_data(story), 'get_story'))

    print(auth.current_user, 'asdfghjkl;nopq')
    pagination = Story.paginate_list(stories, page, per_page)
    stories = pagination['items']
    # re-attach current_user to current session
    # auth.current_user = storage._session.merge(auth.current_user)
    print(stories, ' asdf ')
    return jsonify(
        {
            'total_items': pagination['total_items'],
            'total_pages': pagination['total_pages'],
            'page': pagination['page'],
            'per_page': pagination['per_page'],
            'stories': stories
        }
    ), 200


@views.route(
    '/users/bookmarks/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_bookmarks_of_user():
    if auth.current_user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    stories = []

    for bookmark in auth.current_user.bookmarks:
        stories.append(create_uri(get_story_data(bookmark.story), 'get_story'))

    pagination = Story.paginate_list(stories, page, per_page)
    stories = pagination['items']
    # re-attach current_user to current session
    # auth.current_user = storage._session.merge(auth.current_user)

    return jsonify(
        {
            'total_items': pagination['total_items'],
            'total_pages': pagination['total_pages'],
            'page': pagination['page'],
            'per_page': pagination['per_page'],
            'stories': stories
        }
    ), 200


@views.route(
    '/users/likes/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_likes_of_user():
    if auth.current_user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 8, type=int)
    stories = []

    for like in auth.current_user.likes:
        stories.append(create_uri(get_story_data(like.story), 'get_story'))

    pagination = Story.paginate_list(stories, page, per_page)
    stories = pagination['items']
    # re-attach current_user to current session
    # auth.current_user = storage._session.merge(auth.current_user)
    print(stories, ' asdf ')
    return jsonify(
        {
            'total_items': pagination['total_items'],
            'total_pages': pagination['total_pages'],
            'page': pagination['page'],
            'per_page': pagination['per_page'],
            'stories': stories
        }
    ), 200

@views.route(
    '/users/stories/<int:n>',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def limit_story_of_user(n=None):
    """ Limits the number of stories to get for a particular user

        Attributes:
            - user_id: the id of the user
            - n: a number representing the amount of stories to get

    """

    if auth.current_user is None:
        abort(404)

    # re-attach current_user to current session
    auth.current_user = storage._session.merge(auth.current_user)

    stories = [story for story in auth.current_user.stories]

    limited_stories = {}
    counter = 0
    for story_obj in stories:
        if counter == n:
            break

        limited_stories = [story_obj]
        counter += 1

    return jsonify(
        [
            create_uri(get_story_data(story), 'get_user')
            for story in limited_stories
        ]
    ), 200


@views.route(
    '/users/',
    methods=['DELETE'],
    strict_slashes=False
)
@auth_guard
def delete_user():
    """ Deletes a user """

    if auth.current_user is None:
        abort(404)

    auth.current_user.delete()
    storage.save()
    # reset curret user
    current_user_data = auth.current_user.to_dict()
    auth.current_user = None


    return jsonify({"Deleted": current_user_data}), 200


@views.route(
    '/users/me/',
    methods=['DELETE'],
    strict_slashes=False
)
@auth_guard
def delete_current_user():
    """ Deletes a user """

    if auth.current_user is None:
        abort(404)

    auth.current_user.delete()
    storage.save()
    # reset curret user
    current_user_data = auth.current_user.to_dict()
    auth.current_user = None


    return jsonify({"Deleted": current_user_data}), 200


@views.route(
    '/users/followers',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_user_followers():

    if auth.current_user is None:
        abort(404)

    followers = storage._session.scalars(auth.current_user.followers.select()).all()

    return jsonify([
        get_user_data(follower) for follower in followers
    ])


@views.route(
    '/users/following',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_user_following():

    if auth.current_user is None:
        abort(404)

    followings = storage._session.scalars(auth.current_user.following.select()).all()

    return jsonify([
        get_user_data(following) for following in followings
    ])


@views.route(
    '/users/follow/<string:user_id>',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def follow_or_unfollow_user(user_id=None):
    """ Follow or unfollow a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if auth.current_user is None:
        abort(404)

    if auth.current_user.is_following(user):
        auth.current_user.following.remove(user)
    else:
        auth.current_user.following.add(user)

    storage.save()

    return jsonify(get_user_data(auth.current_user)), 201
