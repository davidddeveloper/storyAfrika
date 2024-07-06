"""
    topics: rest api for quering topics in db or file storage

"""

from flask import request, jsonify, abort, url_for
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from models.topic import Topic
from models.engine import storage


@views.route(
    '/topics/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
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
    '/topics/<string:topic_id>/',
    methods=['GET', 'PUT'],
    strict_slashes=False
)
def get_topic(topic_id=None):
    """ Gets a specific topic or update an existing one """
    topic = storage.get(Topic, topic_id)
    if topic is None:
        abort(404)

    if request.method == 'PUT':
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

    return jsonify(topic.to_dict()), 200


@views.route(
    '/topics/<string:topic_id>/',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_topic(topic_id=None):
    """ Deletes a topic """
    topic = storage.get(Topic, topic_id)

    if topic is None:
        abort(404)

    topic.delete()
    storage.save()
    return jsonify({"Deleted": topic.to_dict()})


@views.route(
    '/topics/<string:topic_id>/stories',
    methods=['GET'],
    strict_slashes=False
)
def get_stories_for_topic(topic_id=None):
    """ all stories under a particular topic

        Attributes:
            - topic_id: the uuid of the topic

    """
    topic = storage.get(Topic, topic_id)

    if topic is None:
        abort(404)

    stories = topic.stories

    return jsonify([
        story.to_dict() for story in stories
    ])


@views.route(
    '/topics/<string:topic_id>/followers',
    methods=['GET'],
    strict_slashes=False
)
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
