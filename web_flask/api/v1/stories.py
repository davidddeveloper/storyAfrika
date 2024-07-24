"""
    stories: rest api for creating stories

"""

import json
from flask import request, jsonify, abort, url_for
from flask_login import current_user, login_required
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from web_flask.api.v1.helper_func import custom_login_required
from models.story import Story
from models.user import User
from models.comment import Comment
from models.like import Like
from models.bookmark import Bookmark
from web_flask.api.v1 import storage


@views.route(
    '/stories/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@login_required
def stories():
    """ Get all stories or creates a story """

    if request.method == 'POST':
        # checks for valid json
        try:
            story_json = request.get_json()
            check_for_valid_json(story_json, ['title', 'text', 'user_id'])

        except Exception:
            return jsonify({"Error": 'not a valid json'}), 400

        else:
            if isinstance(story_json, dict):
                story = Story(
                        title=story_json['title'],
                        text=story_json['text'],
                        user_id=story_json['user_id']
                    )
            elif isinstance(story_json, list):
                story = Story(
                    title=story_json[0],
                    text=story_json[1],
                    user_id=story_json[2]
                )
            storage.new(story)
            storage.save()
            print(story)
            return jsonify(story.to_dict()), 201

    stories = storage.all(Story)

    return jsonify(
        [create_uri(story.to_dict(), 'get_story')
         for story in stories.values()]
    ), 200


@views.route(
        'users/<string:user_id>/following_stories/',
        methods=['GET'],
        strict_slashes=False
)
@login_required
def following_stories(user_id=None):
    """ gets the stories from all the users self is following
        and own stories

    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # query = storage._session.query(Story).where(Story.user_id == user.id)
    query = user.following_stories
    
    pagination = Story.paginate(query, page, per_page)

    stories = []
    for story in pagination['items']:
        is_liked = user.liked_story(story.id)
        story_dictionary = story.to_dict()
        story_dictionary['liked'] = is_liked

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
    '/stories/<int:n>/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@login_required
def limit_stories(n=None):
    """ Limits the number of stories to get

        Attributes:
            - n: a number representing the amount of stories to get

    """

    if n is None:
        abort(404)

    stories = storage.all(Story)
    limited_stories = {}
    counter = 0

    for key, val in stories.items():
        if counter == n:
            break

        limited_stories[key] = val
        counter += 1

    return jsonify(
        [
            create_uri(story.to_dict(), 'get_story')
            for story in limited_stories.values()
        ]
    ), 200


@views.route(
    '/stories/<string:story_id>/',
    methods=['GET', 'PUT'],
    strict_slashes=False
)
@login_required
def get_story(story_id=None):
    """ Gets a specific story or update an existing one """
    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    if request.method == 'PUT':
        try:
            story_json = request.get_json()
            check_for_valid_json(story_json, ['title', 'text', 'user_id'])

        except Exception:
            print('----03')
            return jsonify({"Error": 'not a valid json'}), 400

        else:
            for key, val in story_json.items():
                print('----04', key)
                if key in ['text', 'title']:
                    setattr(story, key, val)

            storage.save()

    return jsonify(story.to_dict()), 200


@views.route(
    '/stories/<string:story_id>/',
    methods=['DELETE'],
    strict_slashes=False
)
@login_required
def delete_story(story_id=None):
    """ Deletes a story """
    story = storage.get(Story, story_id)

    if story is None:
        abort(404)

    story.delete()
    storage.save()
    return jsonify({"Deleted": story.to_dict()})


@views.route(
    '/stories/<string:story_id>/like/',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def like_or_unlike_story(story_id=None):
    """ Like a story

        Attributes:
            - story_id: id of the story

    """

    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    for like in story.likes:
        # user has already like the story
        if like.liker.username == current_user.username:
            # remove the like
            storage.delete(like)
            storage.save()
            return jsonify({'status': 'unliked'}), 201

    # otherwise the user has not like a story
    # like the story
    like = Like(
        story_id=story_id, user_id=current_user.id
    )
    storage.new(like)
    storage.save()

    return jsonify({'status': 'liked'}), 201


@views.route(
    '/stories/<string:story_id>/comments/',
    methods=['POST'],
    strict_slashes=False
)
@login_required
def make_comment_on_story(story_id=None):
    """ Comment on a story

        Attributes:
            - story_id: id of the story

    """
    if story_id is None:
        abort(404)

    try:
        comment_json = request.get_json()
        check_for_valid_json(comment_json, ['comment'])
    except Exception:
        return jsonify({'Error': 'Not a valid json'}), 400

    if isinstance(comment_json, dict):
        comment = Comment(
            comment=comment_json['comment'],
            story_id=story_id,
            user_id=current_user.id
        )
    elif isinstance(comment_json, list):
        comment = Comment(
            comment=comment_json[0],
            story_id=story_id,
            user_id=current_user.id
        )

    storage.new(comment)
    storage.save()

    return jsonify(comment.to_dict()), 201


@views.route(
    '/stories/<string:story_id>/comments',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def get_comments_for_story(story_id=None):
    """ all comments made on a particular story

        Attributes:
            - story_id: the uuid of the story

    """
    story = storage.get(Story, story_id)

    if story is None:
        abort(404)

    comments = story.comments

    return jsonify([
        comment.to_dict() for comment in comments
    ])


@views.route(
    '/stories/<string:story_id>/bookmark/',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def bookmark_or_unbookmark_story(story_id=None):
    """ Bookmark a story

        Attributes:
            - story_id: id of the story

    """

    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    for bookmark in story.bookmark:
        # user has already bookmark the story
        if bookmark.bookmarker.username == current_user.username:
            # remove the bookmark
            storage.delete(bookmark)
            storage.save()
            return jsonify({}), 201

    # otherwise the user has not bookmark a story
    # bookmark the story
    bookmark = Bookmark(
        story_id=story_id, user_id=current_user.id
    )
    storage.new(bookmark)
    storage.save()

    return jsonify({}), 201


@views.route(
    '/stories/<string:story_id>/bookmarks',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def get_bookmarks_for_story(story_id=None):
    """ all bookmarks made on a particular story

        Attributes:
            - story_id: the uuid of the story

    """
    story = storage.get(Story, story_id)

    if story is None:
        abort(404)

    bookmarks = story.bookmarks

    return jsonify([
        bookmark.to_dict() for bookmark in bookmarks
    ])


@views.route(
    '/stories/<string:story_id>/likes',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def get_likes_for_story(story_id=None):
    """ all bookmarks made on a particular story

        Attributes:
            - story_id: the uuid of the story

    """
    story = storage.get(Story, story_id)

    if story is None:
        abort(404)

    likes = story.likes

    return jsonify([
        like.to_dict() for like in likes
    ])


@views.route(
    'liked/<string:story_id>/by/<string:user_id>/',
    methods=['GET'],
    strict_slashes=False
)
@login_required
def check_like(story_id, user_id):
    """ check if a user has liked a story """
    story = storage.get(Story, story_id)
    user = storage.get(User, user_id)

    if story or user is None:
        abort(404)

    return user.liked_story(story.id)

