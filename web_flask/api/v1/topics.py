"""
    topics: rest api for quering topics in db or file storage

"""

from flask import request, jsonify, abort
from flask_login import current_user
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from models.topic import Topic
from models.story import Story
from models.topic_follower import TopicFollower
from web_flask.api.v1 import storage
from web_flask.api.v1.services.data_service import get_story_data
from web_flask.api.v1.services.data_service import get_topic_data
from web_flask.api.v1.services.auth_guard import auth_guard
import web_flask.api.v1.services.auth_provider as auth


@views.route(
    '/topics/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@auth_guard
def topics():
    """ Get all topics or creates a topic """

    if request.method == 'POST':
        # checks for valid json
        try:
            topic_json = request.get_json()
            check_for_valid_json(topic_json, ['name'])

        except Exception:
            return jsonify({"Error": 'not a valid json'}), 400

        else:
            if isinstance(topic_json, dict):
                topic = Topic(
                        name=topic_json['name'],
                        description=topic_json.get('description')
                    )
            elif isinstance(topic_json, list):
                topic = Topic(
                    name=topic_json[0],
                    description=None,
                )
                try:
                    description = topic_json[1]
                    topic.description = description
                except IndexError:
                    pass

            storage.new(topic)
            storage.save()
            print(topic)
            return jsonify(topic.to_dict()), 201

    topics = storage.all(Topic)

    return jsonify(
        [create_uri(topic.to_dict(), 'get_topic') for topic in topics.values()]
    ), 200


@views.route(
    '/topics/<int:n>/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@auth_guard
def limit_topics(n=None):
    """ Limits the number of topics to get

        Attributes:
            - n: a number representing the amount of topics to get

    """

    if n is None:
        abort(404)

    topics = storage.all(Topic)
    limited_topics = {}
    counter = 0

    for key, val in topics.items():
        if counter == n:
            break

        limited_topics[key] = val
        counter += 1

    return jsonify(
        [
            create_uri(topic.to_dict(), 'get_topic')
            for topic in limited_topics.values()
        ]
    ), 200


@views.route(
    '/topics/me/',
    strict_slashes=False,
    methods=['GET']
)
@auth_guard
def get_user_created_topics():
    if not auth.authorize(auth.current_user):
        return jsonify({"Error": "Permission denied!"}), 403
    
    return auth.current_user.topics

@views.route(
    '/topics/<string:topic_id>/',
    methods=['GET', 'PUT'],
    strict_slashes=False
)
@auth_guard
def get_topic(topic_id=None):
    """ Gets a specific topic or update an existing one """
    topic = storage.get(Topic, topic_id)
    if topic is None:
        abort(404)

    return jsonify(get_topic_data(topic)), 200


@views.route(
    '/topics/<string:topic_id>/',
    methods=['PUT'],
    strict_slashes=False
)
@auth_guard
def update_topic(topic_id=None):
    topic = storage.get(Topic, topic_id)

    if topic is None:
        abort(404)

    if not auth.authorize(topic):
        return jsonify({"Error": "Permission denied!"}), 403

    try:
        topic_json = request.get_json()
        check_for_valid_json(topic_json, ['name'])

    except Exception:
        return jsonify({"Error": 'not a valid json'}), 400

    else:
        for key, val in topic_json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(topic, key, val)

        storage.save()


@views.route(
    '/topics/<string:topic_id>/',
    methods=['DELETE'],
    strict_slashes=False
)
@auth_guard
def delete_topic(topic_id=None):
    """ Deletes a topic """
    topic = storage.get(Topic, topic_id)

    if topic is None:
        abort(404)

    if not auth.authorize(topic):
        return jsonify({"Error": "Permission denied!"}), 403

    topic.delete()
    storage.save()
    return jsonify({"Deleted": topic.to_dict()})


@views.route(
    '/topics/<string:topic_id>/stories',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_stories_for_topic(topic_id=None):
    """ all stories under a particular topic

        Attributes:
            - topic_id: the uuid of the topic

    """
    topic = storage.get(Topic, topic_id)
    if topic is None:
        abort(404)

    stories = []

    for story in topic.stories:
        stories.append(get_story_data(story))

    pagination = Topic.paginate_list(stories)
    stories = pagination['items']
    
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
        '/topics/foryou_stories/',
        methods=['GET'],
        strict_slashes=False
)
@auth_guard
def foryou_stories(): # user_id to be removed
    """ gets the stories from all the users self is following
        and own stories

    """
    if auth.current_user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # query = storage._session.query(Story).where(Story.user_id == user.id)
    query = auth.current_user.foryou_stories
    
    pagination = Story.paginate(query, page, per_page)

    stories = []
    for story in pagination['items']:
        stories.append(get_story_data(story))
    
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
    '/topics/<string:topic_id>/followers',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_followers_for_topic(topic_id=None):
    """ all followers made on a particular topic

        Attributes:
            - topic_id: the uuid of the topic

    """
    topic = storage.get(Topic, topic_id)

    if topic is None:
        abort(404)

    followers = topic.followers

    return jsonify([
        follower.to_dict() for follower in followers
    ])


@views.route(
    '/topics/<string:topic_id>/follow/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def follow_or_unfollow_topic(topic_id=None):
    """ Follow or unfollow a topic """
    topic = storage.get(Topic, topic_id)
    if topic is None:
        abort(404)

    for topic_following in current_user.topic_following:
        # login user is already following that topic
        if topic_following.topic_id == topic_id:
            # remove the user from following that topic
            storage.delete(topic_following)
            storage.save()
            return jsonify({}), 201

    # otherwise the login user is not following that topic
    # make the user follow the topic
    topic_follower = TopicFollower(
        user_id=current_user.id,
        topic_id=topic_id
    )
    storage.new(topic_follower)
    storage.save()

    return jsonify({}), 201
