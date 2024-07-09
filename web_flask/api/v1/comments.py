from flask import request, jsonify, abort, url_for
from flask_login import current_user, login_required
from web_flask.api.v1 import views
from web_flask.api.v1.helper_func import create_uri, check_for_valid_json
from web_flask.api.v1.helper_func import custom_login_required
from models.comment import Comment
from web_flask.api.v1 import storage


@views.route(
    '/comments/<string:comment_id>/',
    methods=['DELETE'],
    strict_slashes=False
)
@custom_login_required
def delete_comment_on_story(comment_id=None):
    """ Delete comment on a story

        Attributes:
            - story_id: id of the story

    """
    comment = storage.get(Comment, comment_id)
    if comment is None:
        abort(404)

    storage.delete(comment)
    storage.save()

    return jsonify({}), 201
