from flask import jsonify, abort
from web_flask.api.v1 import views
from models.comment import Comment
from web_flask.api.v1 import storage
from web_flask.api.v1.helper_func import create_uri
from web_flask.api.v1.services.auth_guard import auth_guard
import web_flask.api.v1.services.auth_provider as auth
from web_flask.api.v1.services.data_service import get_comment_data
from sqlalchemy.orm import joinedload


@views.route(
    '/comments/<string:comment_id>/',
    methods=['DELETE'],
    strict_slashes=False
)
@auth_guard
def delete_comment_on_story(comment_id=None):
    """ Delete comment on a story

        Attributes:
            - story_id: id of the story

    """
    comment = storage.get(Comment, comment_id)

    if comment is None:
        abort(404)

    # add current user to current session
    # auth.current_user = storage._session.merge(auth.current_user)

    if not auth.authorize(comment):
        return jsonify({"Error": "Permission denied!"}), 403

    storage.delete(comment)
    storage.save()

    return jsonify({'status': 'deleted'}), 200


@views.route(
    '/comments/<string:comment_id>/',
    methods=['GET'],
    strict_slashes=False
)
@auth_guard
def get_comment_on_story(comment_id=None):
    """ Get comment on a story

        Attributes:
            - story_id: id of the story

    """
    comment = storage.get(Comment, comment_id)

    if comment is None:
        abort(404)
    
    return jsonify(create_uri(get_comment_data(comment), "get_comment_on_story")), 200


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