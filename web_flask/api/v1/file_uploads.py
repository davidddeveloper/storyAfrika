from models.topic import Topic
from web_flask.api.v1.services.auth_guard import auth_guard
import web_flask.api.v1.services.auth_provider as auth
from web_flask.api.v1 import views
from flask import request, abort, jsonify
from models.engine import storage
from models.story import Story
from web_flask.api.v1.services.data_service import get_story_data, get_user_data


@views.route("/stories/<string:story_id>/upload_image/", method=['POST'], strict_slashes=False)
@auth_guard
def upload_image_for_story(story_id=None):
    if story_id is None:
         abort(404)

    story = storage.get(Story, story_id)
    if story is None:
         abort(404)

    if request.files:
            try:
                # save the file
                path_2_file = story.image_upload(request.files['file'], auth.current_user.id)
            except Exception:
                return jsonify({"Error": "Failed to upload image"})
            if path_2_file:
                story.image = path_2_file
                storage.save()
            return jsonify(get_story_data(story)), 200


@views.route("/users/upload_avatar/", methods=['POST'], strict_slashes=False)
@auth_guard
def upload_avater_for_user(user_id=None):
     if user_id is None:
          abort(404)

     if request.files:
            try:
                # save the file
                path_2_file = auth.current_user.image_upload(request.files['file'], auth.current_user.id)
            except Exception:
                return jsonify({"Error": "Failed to upload avatar"})

            if path_2_file:
                auth.current_user.avatar = path_2_file
                storage.save()

            return jsonify(get_user_data(auth.current_user))

@views.route("/topics/<string:topic_id>/upload_banner/", methods=['POST'], strict_slashes=False)
@auth_guard
def upload_image_for_topic(topic_id=None):
    if topic_id is None:
        abort(404)

    topic = storage.get(Topic, topic_id)
    if not topic:
        abort(404)

    if request.files:
        try:
            # save the file
            path_2_file = topic.image_upload(request.files['file'], auth.current_user.id)
        except Exception:
            return jsonify({"Error": "Failed to upload banner"})

        if path_2_file:
            topic.banner = path_2_file
            storage.save()

        return jsonify(get_user_data(auth.current_user))