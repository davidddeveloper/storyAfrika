"""
    stories: rest api for creating stories

"""

import web_flask.api.v1.services.auth_provider as auth
from sqlalchemy.orm import joinedload
from flask import request, jsonify, abort
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from web_flask.api.v1.services.auth_guard import auth_guard
from web_flask.api.v1.services.data_service import get_story_data
from web_flask.api.v1.services.data_service import get_comment_data
from models.story import Story
from models.user import User
from models.comment import Comment
from models.like import Like
from models.bookmark import Bookmark
from models.topic import Topic
from web_flask.api.v1 import storage


@views.route(
    '/stories/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
def stories():
    """ Get all stories or creates a story """

    if request.method == 'POST':
        # checks for valid json
        try:
            story_json = request.get_json()
            check_for_valid_json(story_json, ['title', 'text'])

        except Exception:
            return jsonify({"Error": 'not a valid json'}), 400

        else:
            if isinstance(story_json, dict):
                story = Story(
                        title=story_json['title'],
                        text=story_json['text'],
                        user_id=auth.current_user.id
                    )
            elif isinstance(story_json, list):
                story = Story(
                    title=story_json[0],
                    text=story_json[1],
                    user_id=auth.current_user.id
                )
            storage.new(story)
            storage.save()
            return jsonify(get_story_data(story)), 201

    stories = storage.all(Story)

    return jsonify(
        [create_uri(get_story_data(story), 'get_story')
         for story in stories.values()]
    ), 200


@views.route(
        '/users/following_stories/',
        methods=['GET'],
        strict_slashes=False
)
@auth_guard
def following_stories():
    """ gets the stories from all the users self is following
        and own stories

    """
    if not auth.current_user:
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # query = storage._session.query(Story).where(Story.user_id == user.id)
    query = auth.current_user.following_stories
    
    pagination = Story.paginate(query, page, per_page)

    stories = []
    for story in pagination['items']:
        stories.append(get_story_data(story))

    if stories == []:
        stories = []
        for story in storage.all(Story).values():
            stories.append(get_story_data(story))
            
        pagination = Story.paginate_list(stories)
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
    '/stories/<int:n>/',
    strict_slashes=False,
    methods=['GET', 'POST']
)
@auth_guard
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
            create_uri(get_story_data(story), 'get_story')
            for story in limited_stories.values()
        ]
    ), 200


@views.route(
    '/stories/<string:story_id>/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_story(story_id=None):
    """ Gets a specific story or update an existing one """
    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    # data
    return jsonify(get_story_data(story)), 200


@views.route(
    '/stories/<string:story_id>/',
    methods=['PUT'],
    strict_slashes=False
)
@auth_guard
def update_story(story_id=None):
    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    if not auth.authorize(story):
        return jsonify({"Error": "Permission denied!"}), 403

    try:
        story_json = request.get_json()
        check_for_valid_json(story_json, ['title', 'text'])  # removed check for user_id

    except Exception:
        return jsonify({"Error": 'not a valid json'}), 400

    else:
        for key, val in story_json.items():
            if key in ['text', 'title', 'topics', 'image']:
                if key == 'topics' and val != []:
                    for topic in val:
                        topic_obj = storage._session.query(Topic).where(Topic.name == topic).first()
                        if topic_obj is not None:
                            story.topics.append(topic_obj)
                else:
                    setattr(story, key, val)

        storage.save()
    
    return jsonify(get_story_data(story)), 200

@views.route(
    '/stories/<string:story_id>/',
    methods=['DELETE'],
    strict_slashes=False
)
@auth_guard
def delete_story(story_id=None):
    """ Deletes a story """
    story = storage.get(Story, story_id)

    if story is None:
        abort(404)

    if not auth.authorize(story):
        return jsonify({"Error": "Permission denied!"}), 403

    story.delete()
    storage.save()
    return jsonify({"status": "Deleted"})


@views.route(
    '/stories/<string:story_id>/like/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
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
        if like.liker.username == auth.current_user.username:
            # remove the like
            storage.delete(like)
            storage.save()
            return jsonify({'status': 'unliked', 'likes_count': get_story_data(story).get('likes_count')}), 201

    # otherwise the user has not like a story
    # like the story
    like = Like(
        story_id=story_id, user_id=auth.current_user.id
    )
    storage.new(like)
    storage.save()

    return jsonify({'status': 'liked', 'likes_count': get_story_data(story).get('likes_count')}), 201


@views.route(
    '/users/<string:user_id>/follow/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def follow_or_unfollow(user_id=None):
    """ Follow a story

        Attributes:
            - user_id: id of the user

    """

    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if auth.current_user.is_following(user):
        auth.current_user.unfollow(user)
        status = 'unfollowed'
    else:
        auth.current_user.follow(user)
        status = 'follow'

    storage.save()

    return jsonify({status: status}), 201


@views.route(
    '/stories/<string:story_id>/bookmark/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def bookmark_or_unbookmark_story(story_id=None):
    """ Bookmark a story

        Attributes:
            - story_id: id of the story

    """

    story = storage.get(Story, story_id)
    if story is None:
        abort(404)

    for bookmark in story.bookmarks:
        # user has already bookmark the story
        if bookmark.bookmarker.username == auth.current_user.username:
            # remove the bookmark
            storage.delete(bookmark)
            storage.save()
            return jsonify({}), 201

    # otherwise the user has not bookmark a story
    # bookmark the story
    bookmark = Bookmark(
        story_id=story_id, user_id=auth.current_user.id
    )
    storage.new(bookmark)
    storage.save()

    return jsonify({}), 201


@views.route(
    '/comments/<string:comment_id>/like/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def like_or_unlike_comment(comment_id=None):
    """ Like a comment

        Attributes:
            - comment_id: id of the comment

    """
    from models.engine import storage

    comment = storage._session.query(Comment).options(joinedload(Comment.commenter)).filter_by(id=comment_id).scalar()
    if comment is None:
        abort(404)

    print(comment.is_liked_by(auth.current_user.id), '..................><><><>')
    if not comment.is_liked_by(auth.current_user.id):  # the user has not like a comment
        comment.like(auth.current_user.id)  # like the story
        storage.save()
        return jsonify({'status': 'liked', 'likes_count': get_comment_data(comment).get('likes_count')}), 201
    else:  # user has already like the comment
        comment.unlike(auth.current_user.id)  # unlike it
        storage.save()
        return jsonify({'status': 'unliked', 'likes_count': get_comment_data(comment).get('likes_count')}), 201


@views.route(
    '/stories/<string:story_id>/comments/',
    methods=['POST'],
    strict_slashes=False
)
@auth_guard
def make_comment_on_story(story_id=None):
    """ Comment on a story

        Attributes:
            - story_id: id of the story

    """

    story = storage.get(Story, story_id)
    if story is None or auth.current_user is None:
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
            user_id=auth.current_user.id
        )
    elif isinstance(comment_json, list):
        comment = Comment(
            comment=comment_json[0],
            story_id=story_id,
            user_id=auth.current_user.id
        )

    storage.new(comment)
    storage.save()

    return jsonify(get_comment_data(comment)), 201


@views.route(
    '/stories/<string:story_id>/comments/relevant/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_relevant_comments_for_story(story_id=None):
    """ all comments made on a particular story

        Attributes:
            - story_id: the uuid of the story

    """

    story = storage.get(Story, story_id)

    if story is None or auth.current_user is None:
        abort(404)

    comments_obj = storage._session.execute(story.relevant_comments.options(
        joinedload(Comment.commenter)
    )).scalars().all()
    # import sqlalchemy as sa

    # comments_obj = sa.select(Comment).select_from(story.relevant_comments.subquery())

    # print('------------->', comments_obj)

    # pagination = Comment.paginate(comments_obj, page, per_page)

    # comments = []
    # for comment in pagination['items']:
        # temp = comment.to_dict()
        # temp['is_liked_by'] = comment.is_liked_by(user_id)
        # comments.append(temp)

    # if comments == []:
       # comments_obj = storage._session.execute(story.relevant_comments.options(
       # joinedload(Comment.commenter)
    # )).scalars().all()
    #    _comments = [ comment.to_dict() for comment in comments_obj ]
    #    comments = []
    #    for comment in _comments:
    #        try:
    #            is_liked_by = comment.is_liked_by(story['id'])
    #            comment['is_liked_by'] = is_liked_by
    #            comments.append(story)
    #        except Exception:
    #            pass
    
    # return jsonify(
        #  {
            #  'total_items': pagination['total_items'],
            #  'total_pages': pagination['total_pages'],
            #  'page': pagination['page'],
            #  'per_page': pagination['per_page'],
            #  'stories': comments
        #  }
    #  ), 200
    
    #  print(comments, '-----------------><>--------------')

    return jsonify([
        get_comment_data(comment) for comment in comments_obj
    ])


@views.route(
    '/stories/<string:story_id>/comments/newest/',
    methods=['GET'],
    strict_slashes=False
)
def get_newest_comments_for_story(story_id=None):
    """ all comments made on a particular story

        Attributes:
            - story_id: the uuid of the story

    """
    from models.engine import storage

    story = storage.get(Story, story_id)

    if story is None or auth.current_user is None:
        abort(404)

    comments_obj = storage._session.execute(story.newest_comments.options(
        joinedload(Comment.commenter)
    )).scalars().all()

    return jsonify([
        get_comment_data(comment) for comment in comments_obj
    ])


@views.route(
    '/stories/<string:story_id>/comments/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_comments_for_story(story_id=None):
    """ all comments made on a particular story

        Attributes:
            - story_id: the uuid of the story

    """
    from models.engine import storage

    story = storage.get(Story, story_id)

    if story is None or auth.current_user is None:
        abort(404)

    comments_obj = storage._session.query(Comment).options(
        joinedload(Comment.commenter)
    ).filter_by(story_id=story_id).all()

    return jsonify([
        create_uri(get_comment_data(comment), "get_comment_on_story") for comment in comments_obj
    ])


@views.route(
    '/stories/<string:story_id>/bookmarks',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
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
@auth_guard
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
    '/users/liked/<string:story_id>/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def check_like(story_id=None):
    """ check if a user has liked a story """
    story = storage.get(Story, story_id)

    if not story or auth.current_user is None:
        abort(404)

    return jsonify(auth.current_user.liked_story(story.id)), 200
