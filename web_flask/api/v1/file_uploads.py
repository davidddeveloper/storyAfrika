from models.topic import Topic
from web_flask.api.v1.services.auth_guard import auth_guard
import web_flask.api.v1.services.auth_provider as auth
from web_flask.api.v1 import views
from flask import request, abort, jsonify
from models.engine import storage
from models.story import Story
from web_flask.api.v1.services.data_service import get_story_data, get_user_data
from flask_cors import cross_origin
from models.__init__ import image_upload


@views.route("/stories/<string:story_id>/upload_image/", methods=['POST'], strict_slashes=False)
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
            result = image_upload.upload(request.files['file'], auth.current_user.id)
        except TypeError:
            return jsonify({"Error": "File not supported"})
        except ValueError:
            return jsonify({"Error": "No file receive"})
        #except Exception:
        #    return jsonify({"Error": "Failed to upload image"})

        if result:
            story.image = result.get('image_url')
            storage.save()
            print(story)
        return jsonify(get_story_data(story)), 200
    
    return jsonify({'Error': 'No file sent with request'}), 400


@views.route("/users/upload_avatar/", methods=['POST'], strict_slashes=False)
@auth_guard
def upload_avater_for_user():
     print('received post request', 'thequickbrownfox...')

     if request.files:
        try:
            # save the file
            result = image_upload.upload(request.files['file'], auth.current_user.id)
        except TypeError:
            return jsonify({"Error": "File not supported"})
        except ValueError:
            return jsonify({"Error": "No file receive"})
        except Exception:
            return jsonify({"Error": "Failed to upload avatar"})

        if result:
            auth.current_user.avatar = result.get('image_url')
            storage.save()
            print(auth.current_user)
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

    
@views.route('/x', methods=['POST'])
def some_route():
     print(request)

     return {'status': 200}

@views.route('y')
def some_other_route():
    print(request)

    return {'status': 200}