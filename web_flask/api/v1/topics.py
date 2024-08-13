"""
    topics: rest api for quering topics in db or file storage

"""

from flask import request, jsonify, abort, url_for
from flask_login import current_user, login_required
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from web_flask.api.v1.helper_func import custom_login_required
from models.topic import Topic
from models.user import User
from models.story import Story
from models.topic_follower import TopicFollower
from web_flask.api.v1 import storage


@views.route(
    '/topics/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@custom_login_required
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
    '/topics/<string:topic_id>/<string:user_id>/stories',
    methods=['GET'],
    strict_slashes=False
)
def get_stories_for_topic(topic_id=None, user_id=None):
    """ all stories under a particular topic

        Attributes:
            - topic_id: the uuid of the topic

    """
    topic = storage.get(Topic, topic_id)
    user = storage.get(User, user_id)
    if topic is None or user is None:
        abort(404)

    per_page = request.args.get('per_page', 10, type=int)
    page = request.args.get('page', 1, type=int)

    stories = [st.to_dict() for st in topic.stories]

    for story in stories:
        try:
            story['liked'] = user.liked_story(story['id'])
            story['bookmarked'] = user.bookmarked_story(story['id'])
            writer = storage.get(User, story['writer']['id'])
            story['user_is_following_writer'] = user.is_following(writer)
        except Exception:
            pass

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
        '/topics/<string:user_id>/foryou_stories/',
        methods=['GET'],
        strict_slashes=False
)
#login_required
def foryou_stories(user_id=None):
    """ gets the stories from all the users self is following
        and own stories

    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # query = storage._session.query(Story).where(Story.user_id == user.id)
    query = user.foryou_stories
    
    pagination = Story.paginate(query, page, per_page)

    stories = []
    for story in pagination['items']:
        story_dictionary = story.to_dict()
        story_dictionary['liked'] = user.liked_story(story.id)
        story_dictionary['bookmarked'] = user.bookmarked_story(story.id)
        story_dictionary['user_is_following_writer'] = user.is_following(story.writer)

        stories.append(story_dictionary)
    
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
@custom_login_required
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
