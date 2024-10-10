import web_flask.api.v1.services.auth_provider as auth
from sqlalchemy.orm import joinedload
from flask import request, jsonify, abort
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from web_flask.api.v1.services.auth_guard import auth_guard
from web_flask.api.v1.services.data_service import get_story_data, get_topic_data, get_user_data
from web_flask.api.v1.services.data_service import get_comment_data
from models.story import Story
from models.user import User
from models.comment import Comment
from models.like import Like
from models.bookmark import Bookmark
from models.topic import Topic
from web_flask.api.v1 import storage


@views.route('/search', methods=['POST'], strict_slashes=False)
@auth_guard
def search():
    """ Search STORIES TOPICS STORIES BOOKMARKED USERS """

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    try:
        data = request.get_json()
        print('---------->', data)
        #if 'data' not in data:
            #return jsonify({"Error": "Not a valid json"}), 400

    except Exception:
        return jsonify({"Error": "Not a valid json"}), 400

    if request.args.get('search') == 'stories':
        search = Story.search(data.get('data'))

        # paginate
        pagination = Story.paginate(search, page, per_page)

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
    
    if request.args.get('search') == 'topics':
        search = Topic.search_topics_by_title(data.get('data'))

        return jsonify([create_uri(get_topic_data(topic), 'get_topic') for topic in search.all()]), 200

    if request.args.get('search') == 'stories_bookmarked':
        search = auth.current_user.search_stories_bookmarked(data.get('data'))

        pagination = Bookmark.paginate(search, page, per_page)

        topics = []
        for topic in pagination['items']:
            topics.append(get_story_data(topic))
        
        return jsonify(
            {
                'total_items': pagination['total_items'],
                'total_pages': pagination['total_pages'],
                'page': pagination['page'],
                'per_page': pagination['per_page'],
                'stories': topics
            }
        ), 200
    
    if request.args.get('search') == 'users':
        search = User.search_by_username(data.get('data'))

        pagination = User.paginate(search, page, per_page)

        users = []
        for user in pagination['items']:
            print(user, 'asd105160951515245')
            users.append(get_user_data(user))
        
        return jsonify(
            {
                'total_items': pagination['total_items'],
                'total_pages': pagination['total_pages'],
                'page': pagination['page'],
                'per_page': pagination['per_page'],
                'users': users
            }
        ), 200
    
    # otherwise: search combine and support pagination
    search = data.get('data')

    stories = Story.search(search)
    users = User.search_by_username(search)
    stories_bookmarked = auth.current_user.search_stories_bookmarked(data.get('data'))

    paginated_stories = Story.paginate(stories, page, per_page)
    paginated_users = User.paginate(users, page, per_page)
    paginated_stories_bookmarked = Bookmark.paginate(stories_bookmarked, page, per_page)


    result = {
            "stories": {
                'total_items': paginated_stories['total_items'],
                'total_pages': paginated_stories['total_pages'],
                'page': paginated_stories['page'],
                'per_page': paginated_stories['per_page'],
                'stories': [get_story_data(story) for story in paginated_stories['items']]
            },
            "users": {
                'total_items': paginated_users['total_items'],
                'total_pages': paginated_users['total_pages'],
                'page': paginated_users['page'],
                'per_page': paginated_users['per_page'],
                'users': [get_user_data(story) for story in paginated_users['items']]
            },
            "stories_bookmarked": {
                'total_items': paginated_stories_bookmarked['total_items'],
                'total_pages': paginated_stories_bookmarked['total_pages'],
                'page': paginated_stories_bookmarked['page'],
                'per_page': paginated_stories_bookmarked['per_page'],
                'stories_bookmarked': paginated_stories_bookmarked['items']
            }
        }
    
    return jsonify(result), 200
